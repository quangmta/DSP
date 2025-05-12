import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Các thông số
fs = 1000  # Tăng tần số lấy mẫu lên 1000Hz để có độ phân giải tốt hơn
t = np.arange(0, 2, 1/fs)  # Thời gian từ 0-2s

# Tạo tín hiệu đầu vào với 4 tần số khác nhau
f = np.array([1, 3, 5, 10])  # Các tần số (Hz)
A = np.array([1, 0.7, 0.5, 0.3])  # Biên độ tương ứng
x = (A[0]*np.sin(2*np.pi*f[0]*t) + A[1]*np.sin(2*np.pi*f[1]*t) + 
     A[2]*np.sin(2*np.pi*f[2]*t) + A[3]*np.sin(2*np.pi*f[3]*t))

# Thiết kế các bộ lọc FIR
nyq = fs/2  # Tần số Nyquist
numtaps = 1001  # Tăng số hệ số để có độ dốc tốt hơn ở band transition

# Tạo các bộ lọc
h_low = signal.firwin(numtaps, 3/nyq)  # Thông thấp 3Hz
h_band = signal.firwin(numtaps, [2.5/nyq, 6/nyq], pass_zero=False)  # Thông dải 2.5-6Hz
h_high = signal.firwin(numtaps, 8/nyq, pass_zero=False)  # Thông cao 8Hz

# Lọc tín hiệu
y_low = signal.lfilter(h_low, 1.0, x)
y_band = signal.lfilter(h_band, 1.0, x)
y_high = signal.lfilter(h_high, 1.0, x)

# Tính đáp ứng tần số của các bộ lọc
w_low, h_low_freq = signal.freqz(h_low, worN=8000)
w_band, h_band_freq = signal.freqz(h_band, worN=8000)
w_high, h_high_freq = signal.freqz(h_high, worN=8000)

# Chuyển đổi tần số từ rad/sample sang Hz
freq_resp = w_low * fs / (2*np.pi)

# Tính phổ tần số của tín hiệu
NFFT = len(t)
freq = np.linspace(0, fs/2, NFFT//2)
f_x = np.abs(np.fft.fft(x, NFFT))
f_low = np.abs(np.fft.fft(y_low, NFFT))
f_band = np.abs(np.fft.fft(y_band, NFFT))
f_high = np.abs(np.fft.fft(y_high, NFFT))

# Chuẩn hóa phổ và lấy nửa phổ dương
f_x = f_x[:NFFT//2]/NFFT
f_low = f_low[:NFFT//2]/NFFT
f_band = f_band[:NFFT//2]/NFFT
f_high = f_high[:NFFT//2]/NFFT

# Vẽ tín hiệu trong miền thời gian (2x2)
fig_time = plt.figure(figsize=(15, 10))
fig_time.suptitle('Tín hiệu trong miền thời gian', fontsize=16)

# Tín hiệu gốc
plt.subplot(221)
plt.plot(t, x, 'k-', linewidth=1.5, label='Tín hiệu gốc')
plt.grid(True)
plt.legend(loc='best')
plt.xlabel('Thời gian (s)')
plt.ylabel('Biên độ')
plt.title('Tín hiệu gốc')

# Tín hiệu sau lọc thông thấp
plt.subplot(222)
plt.plot(t, x, 'k--', label='Tín hiệu gốc')
plt.plot(t, y_low, 'r-', linewidth=1.5, label='Sau lọc thông thấp 3Hz')
plt.grid(True)
plt.legend(loc='best')
plt.xlabel('Thời gian (s)')
plt.ylabel('Biên độ')
plt.title('Tín hiệu sau lọc thông thấp')

# Tín hiệu sau lọc thông dải
plt.subplot(223)
plt.plot(t, x, 'k--', label='Tín hiệu gốc')
plt.plot(t, y_band, 'g-', linewidth=1.5, label='Sau lọc thông dải 2.5-6Hz')
plt.grid(True)
plt.legend(loc='best')
plt.xlabel('Thời gian (s)')
plt.ylabel('Biên độ')
plt.title('Tín hiệu sau lọc thông dải')

# Tín hiệu sau lọc thông cao
plt.subplot(224)
plt.plot(t, x, 'k--', label='Tín hiệu gốc')
plt.plot(t, y_high, 'b-', linewidth=1.5, label='Sau lọc thông cao 8Hz')
plt.grid(True)
plt.legend(loc='best')
plt.xlabel('Thời gian (s)')
plt.ylabel('Biên độ')
plt.title('Tín hiệu sau lọc thông cao')

plt.tight_layout()

# Vẽ đáp ứng tần số của bộ lọc
fig_freq = plt.figure(figsize=(15, 10))
fig_freq.suptitle('Đáp ứng tần số của bộ lọc', fontsize=16)

# Đáp ứng biên độ của bộ lọc (dB)
plt.subplot(211)
plt.plot(freq_resp, 20*np.log10(np.abs(h_low_freq)), 'r-', label='Thông thấp 3Hz')
plt.plot(freq_resp, 20*np.log10(np.abs(h_band_freq)), 'g-', label='Thông dải 2.5-6Hz')
plt.plot(freq_resp, 20*np.log10(np.abs(h_high_freq)), 'b-', label='Thông cao 8Hz')
plt.grid(True)
plt.legend(loc='best')
plt.xlabel('Tần số (Hz)')
plt.ylabel('Biên độ (dB)')
plt.title('Đáp ứng biên độ của các bộ lọc')
plt.xlim(0, 15)
plt.ylim(-80, 5)

# Phổ tần số của tín hiệu (dB)
plt.subplot(212)
plt.plot(freq, 20*np.log10(f_x + 1e-10), 'k-', label='Tín hiệu gốc')
plt.plot(freq, 20*np.log10(f_low + 1e-10), 'r-', label='Sau lọc thông thấp')
plt.plot(freq, 20*np.log10(f_band + 1e-10), 'g-', label='Sau lọc thông dải')
plt.plot(freq, 20*np.log10(f_high + 1e-10), 'b-', label='Sau lọc thông cao')
plt.grid(True)
plt.legend(loc='best')
plt.xlabel('Tần số (Hz)')
plt.ylabel('Biên độ (dB)')
plt.title('Phổ tần số của các tín hiệu')
plt.xlim(0, 15)
plt.ylim(-80, 0)

plt.tight_layout()

# Vẽ chi tiết phổ tần số trong các dải quan tâm
fig_detail = plt.figure(figsize=(15, 10))
fig_detail.suptitle('Chi tiết phổ tần số trong các dải quan tâm', fontsize=16)

# Chi tiết dải thông thấp
plt.subplot(311)
plt.plot(freq, 20*np.log10(f_x + 1e-10), 'k--', label='Tín hiệu gốc')
plt.plot(freq, 20*np.log10(f_low + 1e-10), 'r-', linewidth=2, label='Sau lọc thông thấp')
plt.grid(True)
plt.legend(loc='best')
plt.xlabel('Tần số (Hz)')
plt.ylabel('Biên độ (dB)')
plt.title('Chi tiết phổ tần số - Dải thông thấp')
plt.xlim(0, 5)
plt.ylim(-80, 0)

# Chi tiết dải thông dải
plt.subplot(312)
plt.plot(freq, 20*np.log10(f_x + 1e-10), 'k--', label='Tín hiệu gốc')
plt.plot(freq, 20*np.log10(f_band + 1e-10), 'g-', linewidth=2, label='Sau lọc thông dải')
plt.grid(True)
plt.legend(loc='best')
plt.xlabel('Tần số (Hz)')
plt.ylabel('Biên độ (dB)')
plt.title('Chi tiết phổ tần số - Dải thông dải')
plt.xlim(2, 7)
plt.ylim(-80, 0)

# Chi tiết dải thông cao
plt.subplot(313)
plt.plot(freq, 20*np.log10(f_x + 1e-10), 'k--', label='Tín hiệu gốc')
plt.plot(freq, 20*np.log10(f_high + 1e-10), 'b-', linewidth=2, label='Sau lọc thông cao')
plt.grid(True)
plt.legend(loc='best')
plt.xlabel('Tần số (Hz)')
plt.ylabel('Biên độ (dB)')
plt.title('Chi tiết phổ tần số - Dải thông cao')
plt.xlim(7, 12)
plt.ylim(-80, 0)

plt.tight_layout()

# Lưu các hình
fig_time.savefig('time_domain_signals.png', dpi=300, bbox_inches='tight')
fig_freq.savefig('frequency_response.png', dpi=300, bbox_inches='tight')
fig_detail.savefig('frequency_detail.png', dpi=300, bbox_inches='tight')

plt.show()