import numpy as np
import matplotlib.pyplot as plt

# Định nghĩa các tham số
fs = 10  # Tần số lấy mẫu (Hz)
f = 1    # Tần số cơ bản của tín hiệu (Hz)
t = np.arange(0, 2, 1/fs)  # Vector thời gian rời rạc từ 0 đến 2 giây
t_continuous = np.linspace(0, 2, 1000)  # Vector thời gian liên tục với nhiều điểm hơn

# Tạo tín hiệu
x = np.sin(2*np.pi*f*t) + 0.5*np.sin(4*np.pi*f*t)  # Tín hiệu rời rạc
x_continuous = np.sin(2*np.pi*f*t_continuous) + 0.5*np.sin(4*np.pi*f*t_continuous)  # Tín hiệu liên tục

# Tính DFT
X = np.fft.fft(x)
freq = np.fft.fftfreq(len(t), 1/fs)

# Vẽ đồ thị
plt.figure(figsize=(12, 8))

# Subplot 1: Tín hiệu liên tục và rời rạc
plt.subplot(2, 1, 1)
plt.plot(t_continuous, x_continuous, 'b-', label='Tín hiệu liên tục x(t)', alpha=0.5)
plt.stem(t, x, 'r', markerfmt='ro', label='Tín hiệu rời rạc x(n)')
plt.grid(True)
plt.xlabel('Thời gian (s)')
plt.ylabel('Biên độ')
plt.title('Tín hiệu x(t) = sin(2πft) + 0.5sin(4πft)')
plt.legend()

# Subplot 2: Phổ tần số (DFT)
plt.subplot(2, 1, 2)
plt.stem(freq, np.abs(X), 'r', markerfmt='ro', label='Phổ biên độ')
plt.grid(True)
plt.xlabel('Tần số (Hz)')
plt.ylabel('|X(f)|')
plt.title('Phổ tần số của tín hiệu')
plt.legend()

plt.tight_layout()
plt.show() 