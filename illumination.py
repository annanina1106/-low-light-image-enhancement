# Version 1

# import cv2
# import numpy as np

# def process_illumination(img, clip_limit=3.0, gamma_value=None):
#     """
#     Modality A: Illumination
#     1. RGB -> HSV
#     2. V-Channel Gamma Correction (Global Lift) [關鍵步驟]
#     3. CLAHE (Local Contrast)
#     """
#     # 轉換色彩空間 RGB -> HSV
#     hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
#     h, s, v = cv2.split(hsv)

#     # --- 關鍵修正：Gamma 校正 (提升整體基底亮度) ---
#     # 這是為了對抗極度低光源，先將亮度拉回正常線性區間
#     if gamma_value is not None:
#         invGamma = 1.0 / gamma_value
#         table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
#         v = cv2.LUT(v, table)
#     # ---------------------------------------------

#     # 應用 CLAHE
#     if clip_limit is None: clip_limit = 3.0
    
#     clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(8, 8))
#     v_enhanced = clahe.apply(v)

#     return h, s, v, v_enhanced




# Version 2

# import cv2
# import numpy as np

# def process_illumination(img, clip_limit=None, gamma_value=None):
#     """
#     Modality A: Illumination
#     [終極策略] Region-Aware Fusion (區域感知融合)
#     同時解決「背景太暗」與「光源過曝」的問題
#     """
#     # 轉 HSV
#     hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
#     h, s, v = cv2.split(hsv)

#     # 如果外部指定了參數(例如 GUI 手動調整)，就用外部的單一 CLAHE
#     if clip_limit is not None:
#         # 如果有指定 gamma，先做 gamma (相容 GUI 邏輯)
#         if gamma_value is not None and gamma_value != 1.0:
#             invGamma = 1.0 / gamma_value
#             table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
#             v = cv2.LUT(v, table)
            
#         clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(8, 8))
#         v_final = clahe.apply(v)
    
#     else:
#         # === [Auto Mode: 雙路徑融合策略 (最聰明的自適應)] ===
#         print("[Smart Illum] 啟動區域感知融合：分離光源與背景...")
        
#         # 1. 製作「光源遮罩 (Highlight Mask)」
#         # 找出亮度大於 220 的區域 (視為路燈/招牌)
#         _, mask_binary = cv2.threshold(v, 220, 255, cv2.THRESH_BINARY)
        
#         # 2. 柔化遮罩 (Feathering) - 關鍵！避免邊緣生硬
#         mask_blur = cv2.GaussianBlur(mask_binary, (21, 21), 0)
#         mask_weight = mask_blur.astype(float) / 255.0
        
#         # 3. 路徑 A：背景增強版 (Background Layer)
#         # 針對暗部：給予強力補光 (Clip=6.0)，不用擔心燈會爆，因為等一下會被遮住
#         clahe_bg = cv2.createCLAHE(clipLimit=6.0, tileGridSize=(8, 8))
#         v_bg_enhanced = clahe_bg.apply(v)
        
#         # 4. 路徑 B：光源保護版 (Highlight Layer)
#         # 針對亮部：給予輕微補光 (Clip=1.0) 或是直接保留原圖，確保細節清晰
#         clahe_light = cv2.createCLAHE(clipLimit=1.0, tileGridSize=(8, 8))
#         v_light_protected = clahe_light.apply(v)
        
#         # 5. 融合 (Fusion)
#         # 公式：Final = (亮部版 * Mask) + (暗部版 * (1 - Mask))
#         # 意思就是：亮的地方用「保護版」，暗的地方用「增強版」
#         v_final_float = (v_light_protected.astype(float) * mask_weight) + \
#                         (v_bg_enhanced.astype(float) * (1.0 - mask_weight))
                        
#         v_final = np.clip(v_final_float, 0, 255).astype(np.uint8)

#     return h, s, v, v_final





# Version 3

# import cv2
# import numpy as np

# def process_illumination(img, clip_limit=None, gamma_value=None):
#     """
#     Modality A: Illumination
#     [升級版] Region-Aware Fusion + Auto-Gamma
#     解決「不夠亮」的問題：在暗部自動注入 Gamma 增益
#     """
#     # 轉 HSV
#     hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
#     h, s, v = cv2.split(hsv)

#     # === [Manual Mode: 手動模式] ===
#     # 如果外部有指定參數 (例如 GUI 拉動)，就聽 GUI 的
#     if clip_limit is not None:
#         # 如果有指定 gamma，先做 gamma
#         if gamma_value is not None and gamma_value != 1.0:
#             invGamma = 1.0 / gamma_value
#             table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
#             v = cv2.LUT(v, table)
            
#         clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(8, 8))
#         v_final = clahe.apply(v)
    
#     # === [Auto Mode: 自適應全自動模式] ===
#     else:
#         # 1. 計算平均亮度，決定要不要 "預先補光"
#         mean_v = np.mean(v)
#         print(f"[Smart Illum] Scene Mean Brightness: {mean_v:.2f}")

#         # --- 新增：自動 Gamma 增益 (Auto-Gamma) ---
#         # 如果亮度 < 80，代表這張圖偏暗，我們給它一個 Gamma 增益基底
#         # 這樣後面的 CLAHE 才有東西可以拉
#         if mean_v < 80:
#             # 越暗，Gamma 要給越強 (例如 mean=20 -> gamma=2.5, mean=70 -> gamma=1.5)
#             # 動態公式：基礎 1.2 + (80 - mean) * 0.02
#             auto_gamma = 1.5 + (80 - mean_v) * 0.02
#             # 限制最高不要超過 3.0，不然會變全白
#             auto_gamma = min(auto_gamma, 3.0)
            
#             print(f"[Smart Illum] Detected Dark Scene -> Injecting Gamma: {auto_gamma:.2f}")
            
#             invGamma = 1.0 / auto_gamma
#             table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
#             v = cv2.LUT(v, table) # 更新 V 通道，讓它先變亮！
#         # ----------------------------------------

#         # 2. 製作「光源遮罩 (Highlight Mask)」(基於變亮後的 V)
#         # 找出亮度大於 220 的區域 (視為路燈/招牌)
#         _, mask_binary = cv2.threshold(v, 220, 255, cv2.THRESH_BINARY)
#         mask_blur = cv2.GaussianBlur(mask_binary, (21, 21), 0)
#         mask_weight = mask_blur.astype(float) / 255.0
        
#         # 3. 路徑 A：背景增強版 (Background Layer)
#         # 針對暗部：將參數從 6.0 提升到 8.0 (更暴力)
#         # 如果你覺得還是不夠亮，可以把 8.0 改成 10.0
#         clahe_bg = cv2.createCLAHE(clipLimit=8.0, tileGridSize=(8, 8))
#         v_bg_enhanced = clahe_bg.apply(v)
        
#         # 4. 路徑 B：光源保護版 (Highlight Layer)
#         # 針對亮部：維持 1.0 或 1.5，保護細節
#         clahe_light = cv2.createCLAHE(clipLimit=1.5, tileGridSize=(8, 8))
#         v_light_protected = clahe_light.apply(v)
        
#         # 5. 融合 (Fusion)
#         v_final_float = (v_light_protected.astype(float) * mask_weight) + \
#                         (v_bg_enhanced.astype(float) * (1.0 - mask_weight))
                        
#         v_final = np.clip(v_final_float, 0, 255).astype(np.uint8)

#     return h, s, v, v_final




# Version 4
# 去霧優化版

# import cv2
# import numpy as np

# def process_illumination(img, clip_limit=None, gamma_value=None):
#     """
#     Modality A: Illumination (Optimized for Video Clarity)
#     降低 Gamma 上限，避免將極暗噪訊提昇為灰霧。
#     """
#     # 轉 HSV
#     hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
#     h, s, v = cv2.split(hsv)

#     # === [Manual Mode] ===
#     if clip_limit is not None:
#         if gamma_value is not None and gamma_value != 1.0:
#             invGamma = 1.0 / gamma_value
#             table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
#             v = cv2.LUT(v, table)
#         clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(8, 8))
#         v_final = clahe.apply(v)
    
#     # === [Auto Mode] ===
#     else:
#         mean_v = np.mean(v)
        
#         # 1. 自動 Gamma (稍微保守一點，減少灰霧來源)
#         if mean_v < 80:
#             # 原本上限 3.0 改為 2.5，避免過度拉伸底噪
#             auto_gamma = 1.5 + (80 - mean_v) * 0.015 
#             auto_gamma = min(auto_gamma, 2.5) 
            
#             # print(f"[Smart Illum] Gamma: {auto_gamma:.2f}") # Debug用，可註解
            
#             invGamma = 1.0 / auto_gamma
#             table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
#             v = cv2.LUT(v, table)

#         # 2. 光源遮罩
#         _, mask_binary = cv2.threshold(v, 220, 255, cv2.THRESH_BINARY)
#         mask_blur = cv2.GaussianBlur(mask_binary, (21, 21), 0)
#         mask_weight = mask_blur.astype(float) / 255.0
        
#         # 3. 背景增強 (ClipLimit 從 8.0 降回 6.0)
#         # 8.0 雖然很亮，但雜訊太多會變成霧，6.0 比較剛好
#         clahe_bg = cv2.createCLAHE(clipLimit=6.0, tileGridSize=(8, 8))
#         v_bg_enhanced = clahe_bg.apply(v)
        
#         # 4. 光源保護
#         clahe_light = cv2.createCLAHE(clipLimit=1.5, tileGridSize=(8, 8))
#         v_light_protected = clahe_light.apply(v)
        
#         # 5. 融合
#         v_final_float = (v_light_protected.astype(float) * mask_weight) + \
#                         (v_bg_enhanced.astype(float) * (1.0 - mask_weight))
                        
#         v_final = np.clip(v_final_float, 0, 255).astype(np.uint8)

#     return h, s, v, v_final




# Final Version
# 去霧 + 增亮版

import cv2
import numpy as np

def process_illumination(img, clip_limit=None, gamma_value=None):
    """
    Modality A: Illumination (Bright & Clear Version)
    放寬亮度限制，讓畫面更明亮。
    """
    # 轉 HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    # === [Manual Mode] ===
    if clip_limit is not None:
        if gamma_value is not None and gamma_value != 1.0:
            invGamma = 1.0 / gamma_value
            table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
            v = cv2.LUT(v, table)
        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(8, 8))
        v_final = clahe.apply(v)
    
    # === [Auto Mode] ===
    else:
        mean_v = np.mean(v)
        
        # 1. 自動 Gamma (恢復火力)
        if mean_v < 80:
            # 上限調回 3.0，讓極暗場景也能變很亮
            auto_gamma = 1.5 + (80 - mean_v) * 0.02 
            auto_gamma = min(auto_gamma, 3.0) 
            
            invGamma = 1.0 / auto_gamma
            table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
            v = cv2.LUT(v, table)

        # 2. 光源遮罩
        _, mask_binary = cv2.threshold(v, 220, 255, cv2.THRESH_BINARY)
        mask_blur = cv2.GaussianBlur(mask_binary, (21, 21), 0)
        mask_weight = mask_blur.astype(float) / 255.0
        
        # 3. 背景增強 (ClipLimit 調回 8.0)
        # 讓背景更亮，雖然會有些許雜訊，但亮度優先
        clahe_bg = cv2.createCLAHE(clipLimit=8.0, tileGridSize=(8, 8))
        v_bg_enhanced = clahe_bg.apply(v)
        
        # 4. 光源保護 (稍微放寬一點到 2.0，讓路燈周圍也亮一點)
        clahe_light = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        v_light_protected = clahe_light.apply(v)
        
        # 5. 融合
        v_final_float = (v_light_protected.astype(float) * mask_weight) + \
                        (v_bg_enhanced.astype(float) * (1.0 - mask_weight))
                        
        v_final = np.clip(v_final_float, 0, 255).astype(np.uint8)

    return h, s, v, v_final