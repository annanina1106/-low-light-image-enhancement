# Version 1

# import cv2
# import numpy as np

# def fuse_images(h, s, v_enhanced, structure_map, structure_weight=0.2):
#     """
#     Fusion Strategy:
#     1. 融合: Enhanced V + (weight * Structure)
#     2. 還原: 合併 H, S, New_V -> RGB
#     """
    
#     # [cite: 28] 融合策略
#     # 將型態轉為 float 進行計算，避免溢位
#     v_fused_float = v_enhanced.astype(float) + (structure_map.astype(float) * structure_weight)
    
#     # 限制數值在 0-255 之間並轉回 uint8
#     v_fused = np.clip(v_fused_float, 0, 255).astype(np.uint8)

#     # [cite: 29] 色彩還原
#     # 這裡可以選擇是否要稍微增強 S (飽和度) 以避免色彩平淡
#     # s_boosted = cv2.addWeighted(s, 1.2, s, 0, 0) 
    
#     # 合併通道
#     final_hsv = cv2.merge((h, s, v_fused))
    
#     # 轉回 RGB (BGR for OpenCV)
#     final_bgr = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    
#     return final_bgr





# Version 2

# import cv2
# import numpy as np

# def fuse_images(h, s, v_enhanced, structure_map, structure_weight=None):
#     """
#     Fusion Strategy (Updated for De-hazing)
#     1. 自適應權重融合
#     2. [新功能] 飽和度補償 (解決色彩平淡)
#     3. [新功能] 智慧對比度拉伸 (解決畫面灰灰的)
#     """
    
#     # === 1. 自適應結構權重邏輯 (保持不變) ===
#     if structure_weight is None:
#         std_v = np.std(v_enhanced)
#         if std_v > 45:
#             structure_weight = 0.4
#         else:
#             structure_weight = 0.1
#     # ======================================

#     # 融合亮度與結構
#     v_fused_float = v_enhanced.astype(float) + (structure_map.astype(float) * structure_weight)
#     v_fused = np.clip(v_fused_float, 0, 255).astype(np.uint8)

#     # === [關鍵修正 1] 飽和度補償 (Saturation Boost) ===
#     # 因為亮度提昇了，飽和度也要跟著提升，不然會泛白
#     # 這裡將 S 通道乘上 1.3 倍 (你可以調整這個數值，1.2 ~ 1.5 都不錯)
#     s_boost = cv2.addWeighted(s, 1.3, s, 0, 0)

#     # 合併通道
#     final_hsv = cv2.merge((h, s_boost, v_fused))
#     final_bgr = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)

#     # === [關鍵修正 2] 智慧對比度拉伸 (De-hazing / Contrast Stretch) ===
#     # 這一步專門用來消除「灰霧感」
#     # 原理：把暗部壓更暗 (beta<0)，把亮部拉更亮 (alpha>1)
#     # alpha=1.1 (對比度增加 10%), beta=-10 (亮度整體減 10，把灰色壓回黑色)
#     final_bgr = cv2.convertScaleAbs(final_bgr, alpha=1.1, beta=-15)

#     return final_bgr





# Version 3

# import cv2
# import numpy as np

# def fuse_images(h, s, v_enhanced, structure_map, structure_weight=None):
#     """
#     Fusion Strategy (Updated for De-hazing)
#     1. 自適應權重融合
#     2. [新功能] 飽和度補償 (解決色彩平淡)
#     3. [新功能] 智慧對比度拉伸 (解決畫面灰灰的)
#     """
    
#     # === 1. 自適應結構權重邏輯 (保持不變) ===
#     if structure_weight is None:
#         std_v = np.std(v_enhanced)
#         if std_v > 45:
#             structure_weight = 0.25
#         else:
#             structure_weight = 0.1
#     # ======================================

#     # 融合亮度與結構
#     v_fused_float = v_enhanced.astype(float) + (structure_map.astype(float) * structure_weight)
#     v_fused = np.clip(v_fused_float, 0, 255).astype(np.uint8)

#     # === [關鍵修正 1] 飽和度補償 (Saturation Boost) ===
#     # 因為亮度提昇了，飽和度也要跟著提升，不然會泛白
#     # 這裡將 S 通道乘上 1.3 倍 (你可以調整這個數值，1.2 ~ 1.5 都不錯)
#     s_boost = cv2.addWeighted(s, 1.3, s, 0, 0)

#     # 合併通道
#     final_hsv = cv2.merge((h, s_boost, v_fused))
#     final_bgr = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)

#     # === [關鍵修正 2] 智慧對比度拉伸 (De-hazing / Contrast Stretch) ===
#     # 這一步專門用來消除「灰霧感」
#     # 原理：把暗部壓更暗 (beta<0)，把亮部拉更亮 (alpha>1)
#     # alpha=1.1 (對比度增加 10%), beta=-10 (亮度整體減 10，把灰色壓回黑色)
#     final_bgr = cv2.convertScaleAbs(final_bgr, alpha=1.1, beta=-15)

#     return final_bgr




# Version 4
# 去霧優化版

# import cv2
# import numpy as np

# def fuse_images(h, s, v_enhanced, structure_map, structure_weight=None):
#     """
#     Fusion Strategy (Updated for De-hazing V2 - Aggressive)
#     1. 自適應權重融合
#     2. [加強] 飽和度補償 (Saturation Boost)
#     3. [加強] 暴力去霧 (Aggressive De-hazing)
#     """
    
#     # === 1. 自適應結構權重邏輯 ===
#     if structure_weight is None:
#         std_v = np.std(v_enhanced)
#         if std_v > 45:
#             structure_weight = 0.25
#         else:
#             structure_weight = 0.1
    
#     # 融合亮度與結構
#     v_fused_float = v_enhanced.astype(float) + (structure_map.astype(float) * structure_weight)
#     v_fused = np.clip(v_fused_float, 0, 255).astype(np.uint8)

#     # === [關鍵修正 1] 更強的飽和度補償 ===
#     # 灰霧會吃掉顏色，所以我們要暴力一點補回來
#     # 使用 multiply 比較直觀：S 通道 * 1.5 倍
#     s_float = s.astype(float) * 1.5 
#     s_boost = np.clip(s_float, 0, 255).astype(np.uint8)

#     # 合併通道
#     final_hsv = cv2.merge((h, s_boost, v_fused))
#     final_bgr = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)

#     # === [關鍵修正 2] 暴力去霧 (Aggressive De-hazing) ===
#     # 這裡的參數調整是為了消除 "洗白/灰濛濛" 的感覺
#     # alpha=1.25: 對比度增加 25% (讓亮的更亮)
#     # beta=-30:   亮度扣除 30 (把深灰色強制壓成純黑) -> 這是去霧的核心！
#     final_bgr = cv2.convertScaleAbs(final_bgr, alpha=1.25, beta=-30)

#     return final_bgr




# Final Version
# 去霧 + 增亮版

import cv2
import numpy as np

def fuse_images(h, s, v_enhanced, structure_map, structure_weight=None):
    """
    Fusion Strategy (Updated for Brightness Recovery)
    1. 降低去霧強度，改用 Gamma 提亮
    2. 保持黑色純淨，同時提升整體亮度
    """
    
    # === 1. 自適應結構權重邏輯 ===
    if structure_weight is None:
        std_v = np.std(v_enhanced)
        if std_v > 45:
            structure_weight = 0.25
        else:
            structure_weight = 0.1
    
    # 融合
    v_fused_float = v_enhanced.astype(float) + (structure_map.astype(float) * structure_weight)
    v_fused = np.clip(v_fused_float, 0, 255).astype(np.uint8)

    # === [關鍵修正 1] 飽和度 (維持 1.5 倍) ===
    s_float = s.astype(float) * 1.5 
    s_boost = np.clip(s_float, 0, 255).astype(np.uint8)

    # 合併通道
    final_hsv = cv2.merge((h, s_boost, v_fused))
    final_bgr = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)

    # === [關鍵修正 2] 亮度回補策略 ===
    
    # A. 輕微去霧 (beta 從 -30 改回 -10)
    # 這樣就不會把畫面壓得太暗
    final_bgr = cv2.convertScaleAbs(final_bgr, alpha=1.1, beta=-10)
    
    # B. Gamma 提亮 (Magic Touch!)
    # 建立 Gamma=0.8 的曲線 (數值越小越亮，0.8 是一個很棒的平衡點)
    # 這會把暗部細節拉亮，但不會把純黑變成灰
    invGamma = 1.0 / 0.8 
    table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
    final_bgr = cv2.LUT(final_bgr, table)

    return final_bgr