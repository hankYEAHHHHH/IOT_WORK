# 使用你的 GPIO 接線，提供老師 IoT_Course 設定及 Hank 重構版相容名稱。
# 低光復歸門檻 150 為初始建議值，請依實測調整。
"""
config.py - 全域配置文件
集中管理所有硬體腳位、MQTT 設定、WiFi 設定等
"""

# ==================== 硬體腳位配置 ====================

# LED 腳位配置（GPIO）
LED_RED_PIN = 25
LED_GREEN_PIN = 14
LED_BLUE_PIN = 13

# 按鈕腳位配置（GPIO）
BUTTON1_PIN = 32
BUTTON2_PIN = 33

# 感測器腳位配置
DHT11_PIN = 27
TEMT_ADC_PIN = 34
PIR_PIN = 26
SPEAKER_PIN = 16

# I2C 配置（OLED）
I2C_ID = 0
I2C_SCL_PIN = 22
I2C_SDA_PIN = 21
OLED_WIDTH = 128
OLED_HEIGHT = 64

# SPI 配置（RFID）
RFID_SCK_PIN = 18
RFID_MOSI_PIN = 23
RFID_MISO_PIN = 19
RFID_RST_PIN = 17
RFID_CS_PIN = 5

# ==================== 感測器參數 ====================

# 光感測器閾值
# LED 控制模式：AUTO 允許光感低光警示；MANUAL 不由光感覆蓋使用者命令
LED_CONTROL_MODE = 'AUTO'
LIGHT_ALERT_ENABLED = True
LIGHT_ALERT_TRIGGER_ADC = 100  # 嚴格低於此值觸發一次
LIGHT_ALERT_RESET_ADC = 150    # 回升至此值以上才允許下一次
LIGHT_ALERT_BLINK_COUNT = 5
LIGHT_ALERT_ON_MS = 300
LIGHT_ALERT_OFF_MS = 300
LIGHT_POLL_INTERVAL_MS = 50    # 光感測輪詢間隔

# DHT11 量測間隔
DHT11_POLL_INTERVAL_SEC = 2

# OLED 更新間隔
OLED_UPDATE_INTERVAL_SEC = 1

# RFID 讀卡間隔（避免反應過快）
RFID_POLL_INTERVAL_MS = 500

# PIR 移動提示：每次低→高觸發，音符時間單位為秒
PIR_POLL_INTERVAL_MS = 100
PIR_HIGH_DEBOUNCE_MS = 200
PIR_LOW_REARM_MS = 1500
MOTION_DETECTED_HOLD_MS = 5000  # 網頁狀態顯示保持時間，不是PIR去重時間
SPEAKER_DUTY = 512
MOTION_MELODY = (('C4', 0.3), ('E4', 0.3), ('D4', 0.3),
                 ('G3', 0.3), ('REST', 0.2))

# 按鈕去彈跳時間
BUTTON_DEBOUNCE_MS = 20         # 按鈕穩定判定時間
BUTTON_POLL_INTERVAL_MS = 30    # 按鈕輪詢間隔

# ==================== WiFi 配置 ====================

# 已知 WiFi 網路清單（SSID: 密碼）
WIFI_PROFILES = {
    'WTF': '00000000',
}

# 時區設定（UTC+8 for Taiwan）
TIMEZONE_OFFSET_SEC = 8 * 3600

# ==================== MQTT 配置 ====================

# MQTT Broker 設定
MQTT_BROKER = 'broker.emqx.io'
MQTT_PORT = 1883

# MQTT Topic 配置
MQTT_TOPICS = {
    'cmd': b'hank_esp32_2026/cmd',           # 接收指令
    'temp_humi': b'hank_esp32_2026/dht11',  # 發佈溫濕度
    'subscribe': b'hank_esp32_2026/#',         # 訂閱所有
}

# MQTT 重連設定
MQTT_RECONNECT_INITIAL_DELAY_SEC = 2     # 初始重連延遲
MQTT_RECONNECT_MAX_DELAY_SEC = 60        # 最大重連延遲
MQTT_RECONNECT_BACKOFF_FACTOR = 1.5      # 指數退避因子

# ==================== 字體配置 ====================

FONT_PATH = './lib/fonts/fusion_bdf.12'

# ==================== 顏色對應 ====================

# RGB LED 8 色對應 (3-bit: RGB)
COLOR_MAP = {
    0: ('黑', 0b000),
    1: ('藍', 0b001),
    2: ('綠', 0b010),
    3: ('青', 0b011),
    4: ('紅', 0b100),
    5: ('紫', 0b101),
    6: ('黃', 0b110),
    7: ('白', 0b111),
}

# ==================== 裝置識別 ====================

DEVICE_NAME = 'Hank 的 IoT 裝置'
DEVICE_ID = 'esp32_hank_final'

# ==================== Hank 重構版相容名稱 ====================
RED_PIN = LED_RED_PIN
GREEN_PIN = LED_GREEN_PIN
BLUE_PIN = LED_BLUE_PIN
DHT_PIN = DHT11_PIN
LIGHT_PIN = TEMT_ADC_PIN
BUZZER_PIN = SPEAKER_PIN
OLED_SCL = I2C_SCL_PIN
OLED_SDA = I2C_SDA_PIN
RFID_SCK = RFID_SCK_PIN
RFID_MOSI = RFID_MOSI_PIN
RFID_MISO = RFID_MISO_PIN
RFID_RST = RFID_RST_PIN
RFID_CS = RFID_CS_PIN
SSID = 'WTF'
PASSWORD = WIFI_PROFILES[SSID]
BROKER = MQTT_BROKER
CLIENT_ID = DEVICE_ID
TOPIC = MQTT_TOPICS["temp_humi"]
LIGHT_THRESHOLD = LIGHT_ALERT_TRIGGER_ADC
