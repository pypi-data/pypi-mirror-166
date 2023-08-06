from einops import rearrange
import numpy as np
import pytorch_lightning as pl
import torch
import torch.nn as nn
import torchaudio.transforms as tat
from torch.nn import TransformerEncoderLayer, TransformerEncoder


def build_encoder(embed_dim, n_heads, dim_feedforward, dropout, n_layers):
    assert (embed_dim % n_heads) == 0, f'Transformers embed_dim must be divisible by n_heads but' \
                                   f' {embed_dim}/{n_heads}={embed_dim // n_heads}R{embed_dim % n_heads}'
    layer = TransformerEncoderLayer(embed_dim, n_heads, dim_feedforward, dropout, activation='gelu')
    encoder = TransformerEncoder(layer, n_layers, norm=nn.LayerNorm(embed_dim))
    return encoder


def get_sinusoid_encoding_table(n_position, d_hid, padding_idx=None):
    """ Sinusoid position encoding table """

    def cal_angle(position, hid_idx):
        return position / np.power(10000, 2 * (hid_idx // 2) / d_hid)

    def get_posi_angle_vec(position):
        return [cal_angle(position, hid_j) for hid_j in range(d_hid)]

    sinusoid_table = np.array([get_posi_angle_vec(pos_i) for pos_i in range(n_position)])

    sinusoid_table[:, 0::2] = np.sin(sinusoid_table[:, 0::2])  # dim 2i
    sinusoid_table[:, 1::2] = np.cos(sinusoid_table[:, 1::2])  # dim 2i+1

    if padding_idx is not None:
        # zero vector for padding dimension
        sinusoid_table[padding_idx] = 0.

    return torch.FloatTensor(sinusoid_table)


class AST(pl.LightningModule):
    """Audio Spectrogram Transformer"""

    def __init__(self, cfg):
        super().__init__()

        self.augmentation = nn.Sequential(
            tat.TimeMasking(cfg.n_mel // 4, iid_masks=True),
            tat.FrequencyMasking(cfg.melspec_len // 4, iid_masks=True),
        )

        self.patch_linear_projection = nn.Conv2d(1, cfg.embed_dim, kernel_size=(16, 16), stride=(10, 10))
        self.pos_emb = nn.Embedding.from_pretrained(
            get_sinusoid_encoding_table(cfg.input_seq_len + 1, cfg.embed_dim, padding_idx=0),
            freeze=True)
        self.transformer_encoder = build_encoder(cfg.embed_dim,
                                                 cfg.n_heads,
                                                 cfg.dim_feedforward,
                                                 cfg.dropout,
                                                 cfg.n_layers)
        self.pooling = nn.AdaptiveAvgPool1d(1)
        self.linear_output = nn.Sequential(
            nn.LayerNorm(cfg.embed_dim),
            nn.Linear(cfg.embed_dim, cfg.n_classes))
        self.activation = nn.Softmax(dim=-1)

    def forward(self, data):
        """get valid raw logits from a batch of melspecs"""
        data = data.float() # B T C

        data = rearrange(data, 'b t c -> b c t')

        """
        if self.training:
            with torch.no_grad():
                data = torch.unsqueeze(data, 1)
                data = self.augmentation(data)
                data = torch.squeeze(data) # B C T
        """

        data = data.unsqueeze(1) # B 1 C T
        proj_patches = self.patch_linear_projection(data)
        proj_patches = rearrange(proj_patches, 'b c w t -> b (t w) c')
        B, T, C = proj_patches.shape
        pos = torch.arange(1, T + 1, device=proj_patches.device)
        pos = self.pos_emb(pos)
        proj_patches += pos.unsqueeze(0)
        encodings = self.pooling(self.transformer_encoder(proj_patches).permute(0, 2, 1)).squeeze()
        logits = self.linear_output(encodings)
        return logits
