import os
from PIL import Image, ImageDraw, ImageFont

# —— 参数区 —— #
image_paths = [
    "images/velocity_quiver__00000_fluid_nosigma.png",
    "images/velocity_quiver__00000_fluid.png",
    "images/velocity_quiver__00000_balls_nosigma.png",
    "images/velocity_quiver__00000_balls.png",
    "images/tsne_gaussians_orig_test_balls.png",
    "images/tsne_gaussians_def_test_balls.png",
    "images/tsne_gaussians_orig_test_grid4d.png",
    "images/tsne_gaussians_def_test_grid4d.png",
]

# 在这里填入你自己的 8 个标题（与上面路径一一对应）
titles = [
    "Velocity Flow in Fluid (no sigma)",
    "Velocity Flow in Fluid (with sigma)",
    "Velocity Flow in Collision (no sigma)",
    "Velocity Flow in Collision (with sigma)",
    "t-SNE of Canonical Gaussians (Ours)",
    "t-SNE of Deformable Gaussians (Ours)",
    "t-SNE of Canonical Gaussians (Grid4D)",
    "t-SNE of Deformable Gaussians (Grid4D)",
]

output_path  = "images/exp_pidg.png"
font_path    = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
font_size    = 48
title_height = 60
spacing      = 10

font = ImageFont.truetype(font_path, font_size)

# 1. 找出最大宽度
orig_sizes = [Image.open(p).size for p in image_paths]
max_w = max(w for w, h in orig_sizes)

# 2. 等宽缩放 + 加自定义标题
annotated = []
for idx, img_path in enumerate(image_paths):
    orig = Image.open(img_path).convert("RGBA")
    w0, h0 = orig.size

    # 等宽缩放
    if w0 != max_w:
        new_h = int(h0 * (max_w / w0))
        img = orig.resize((max_w, new_h), Image.LANCZOS)
    else:
        img, new_h = orig, h0

    # 顶部留白并粘贴
    canvas = Image.new("RGBA", (max_w, new_h + title_height), (255,255,255,255))
    canvas.paste(img, (0, title_height))

    draw = ImageDraw.Draw(canvas)
    title = titles[idx]  # ← 使用自定义标题列表
    bbox = draw.textbbox((0,0), title, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]

    draw.text(
        ((max_w - tw)//2, (title_height - th)//2),
        title,
        fill="black",
        font=font
    )
    annotated.append(canvas)

# 3. 统一高度填充
cell_h = max(im.height for im in annotated)
uniform = []
for im in annotated:
    if im.height < cell_h:
        pad = Image.new("RGBA", (max_w, cell_h), (255,255,255,255))
        pad.paste(im, (0, 0), im)
        uniform.append(pad)
    else:
        uniform.append(im)

# 4. 4×2 网格拼接
grid_w = 4 * max_w + spacing * 3
grid_h = 2 * cell_h + spacing * 1
combined = Image.new("RGBA", (grid_w, grid_h), (255,255,255,255))
for idx, im in enumerate(uniform):
    row, col = divmod(idx, 4)
    x = col * (max_w + spacing)
    y = row * (cell_h + spacing)
    combined.paste(im, (x, y), im)

combined.save(output_path)
print(f"4×2 网格拼接完成，已保存到 {output_path}")
