#define APDS9960_I2C_ADDRESS 0x39 << 1

// Định nghĩa các thanh ghi của APDS-9960
#define APDS9960_ENABLE 0x80
#define APDS9960_ATIME 0x81
#define APDS9960_WTIME 0x83
#define APDS9960_PPULSE 0x8E
#define APDS9960_CONTROL 0x8F
#define APDS9960_ID 0x92
#define APDS9960_PDATA 0x9C

extern I2C_HandleTypeDef hi2c1;

void APDS9960_WriteRegister(uint8_t reg, uint8_t value)
{
  uint8_t data[2];
  data[0] = reg;
  data[1] = value;
  HAL_I2C_Master_Transmit(&hi2c1, APDS9960_I2C_ADDRESS, data, 2, 100);
}

uint8_t APDS9960_ReadRegister(uint8_t reg)
{
  uint8_t value;
  HAL_I2C_Master_Transmit(&hi2c1, APDS9960_I2C_ADDRESS, &reg, 1, 100);
  HAL_I2C_Master_Receive(&hi2c1, APDS9960_I2C_ADDRESS, &value, 1, 100);
  return value;
}

void APDS9960_Init(void)
{
  // Khởi tạo cảm biến
  APDS9960_WriteRegister(APDS9960_ENABLE, 0x00); // Tắt tất cả các tính năng
  APDS9960_WriteRegister(APDS9960_ATIME, 0xFF); // Thiết lập thời gian tích hợp ADC
  APDS9960_WriteRegister(APDS9960_WTIME, 0xFF); // Thiết lập thời gian chờ
  APDS9960_WriteRegister(APDS9960_PPULSE, 0x87); // Thiết lập độ rộng xung phát hồng ngoại
  APDS9960_WriteRegister(APDS9960_CONTROL, 0x20); // Thiết lập gain
  APDS9960_WriteRegister(APDS9960_ENABLE, 0x05); // Bật cảm biến khoảng cách
}

uint8_t APDS9960_ReadProximity(void)
{
  uint8_t proximity;
  proximity = APDS9960_ReadRegister(APDS9960_PDATA);
  return proximity;
}

int main(void)
{
  HAL_Init();
  SystemClock_Config();
  MX_GPIO_Init();
  MX_I2C1_Init();

  // Khởi tạo APDS-9960
  APDS9960_Init();

  while (1)
  {
    // Đọc dữ liệu khoảng cách từ APDS-9960
    uint8_t proximity = APDS9960_ReadProximity();
    HAL_Delay(500); // Đợi 500ms trước khi đọc lại
  }
}


# #include "main.h"

# #define APDS9960_I2C_ADDRESS    (0x39 << 1)

# // Định nghĩa các thanh ghi của APDS-9960
# #define APDS9960_ENABLE         0x80
# #define APDS9960_ATIME          0x81
# #define APDS9960_WTIME          0x83
# #define APDS9960_PPULSE         0x8E
# #define APDS9960_CONTROL        0x8F
# #define APDS9960_ID             0x92
# #define APDS9960_PDATA          0x9C
# #define APDS9960_GFIFO_U        0xFC

# I2C_HandleTypeDef hi2c1;

# void APDS9960_Init(void)
# {
    # uint8_t data;

    # // Tắt tất cả các tính năng trước khi cấu hình
    # data = 0x00;
    # HAL_I2C_Mem_Write(&hi2c1, APDS9960_I2C_ADDRESS, APDS9960_ENABLE, 1, &data, 1, 100);

    # // Thiết lập thời gian tích hợp ADC
    # data = 0xFF;
    # HAL_I2C_Mem_Write(&hi2c1, APDS9960_I2C_ADDRESS, APDS9960_ATIME, 1, &data, 1, 100);

    # // Thiết lập thời gian chờ
    # data = 0xFF;
    # HAL_I2C_Mem_Write(&hi2c1, APDS9960_I2C_ADDRESS, APDS9960_WTIME, 1, &data, 1, 100);

    # // Thiết lập độ rộng xung phát hồng ngoại
    # data = 0x87;
    # HAL_I2C_Mem_Write(&hi2c1, APDS9960_I2C_ADDRESS, APDS9960_PPULSE, 1, &data, 1, 100);

    # // Thiết lập gain
    # data = 0x20;
    # HAL_I2C_Mem_Write(&hi2c1, APDS9960_I2C_ADDRESS, APDS9960_CONTROL, 1, &data, 1, 100);

    # // Bật cảm biến khoảng cách và các tính năng cần thiết khác
    # data = 0x05;
    # HAL_I2C_Mem_Write(&hi2c1, APDS9960_I2C_ADDRESS, APDS9960_ENABLE, 1, &data, 1, 100);
# }

# uint8_t APDS9960_ReadRegister(uint8_t reg)
# {
    # uint8_t value;
    # HAL_I2C_Mem_Read(&hi2c1, APDS9960_I2C_ADDRESS, reg, 1, &value, 1, 100);
    # return value;
# }

# void APDS9960_ReadGesture(uint8_t *gesture_data_array)
# {
    # HAL_I2C_Mem_Read(&hi2c1, APDS9960_I2C_ADDRESS, APDS9960_GFIFO_U, 1, gesture_data_array, 4, 100);
# }

# int main(void)
# {
    # HAL_Init();
    # SystemClock_Config();
    # MX_GPIO_Init();
    # MX_I2C1_Init();

    # // Khởi tạo cảm biến APDS-9960
    # APDS9960_Init();

    # // Biến để lưu trữ dữ liệu cử chỉ
    # uint8_t gesture_data_array[4];

    # while (1)
    # {
        # // Đọc dữ liệu từ FIFO của cảm biến APDS-9960
        # APDS9960_ReadGesture(gesture_data_array);

        # // Kiểm tra và xử lý các cử chỉ
        # for (int i = 0; i < 4; ++i)
        # {
            # uint8_t gesture_up = gesture_data_array[i] & 0b00000001;
            # uint8_t gesture_down = gesture_data_array[i] & 0b00000010;
            # uint8_t gesture_left = gesture_data_array[i] & 0b00000100;
            # uint8_t gesture_right = gesture_data_array[i] & 0b00001000;

            # // Xử lý các cử chỉ
            # if (gesture_up)
            # {
                # // Xử lý cử chỉ lên
                # // Ví dụ: Toggle một GPIO, gửi tin nhắn qua UART, ...
            # }

            # if (gesture_down)
            # {
                # // Xử lý cử chỉ xuống
                # // Ví dụ: Toggle một GPIO, gửi tin nhắn qua UART, ...
            # }

            # if (gesture_left)
            # {
                # // Xử lý cử chỉ trái
                # // Ví dụ: Toggle một GPIO, gửi tin nhắn qua UART, ...
            # }

            # if (gesture_right)
            # {
                # // Xử lý cử chỉ phải
                # // Ví dụ: Toggle một GPIO, gửi tin nhắn qua UART, ...
            # }
        # }

        # HAL_Delay(100); // Đợi một khoảng thời gian trước khi đọc lại
    # }
# }
