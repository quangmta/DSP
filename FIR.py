import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Các thông số
fs = 100  # Tần số lấy mẫu (Hz)
t = np.arange(0, 2, 1/fs)  # Thời gian từ 0-2s

# Tạo tín hiệu đầu vào với 4 tần số khác nhau
f = np.array([1, 3, 5, 10])  # Các tần số (Hz)
A = np.array([1, 0.7, 0.5, 0.3])  # Biên độ tương ứng
x = (A[0]*np.sin(2*np.pi*f[0]*t) + A[1]*np.sin(2*np.pi*f[1]*t) + 
     A[2]*np.sin(2*np.pi*f[2]*t) + A[3]*np.sin(2*np.pi*f[3]*t))

# Thiết kế các bộ lọc FIR
nyq = fs/2  # Tần số Nyquist
numtaps = 101  # Số hệ số của bộ lọc

# Tạo các bộ lọc
h_low = signal.firwin(numtaps, 3/nyq)  # Thông thấp 3Hz
h_band = signal.firwin(numtaps, [2.5/nyq, 6/nyq], pass_zero=False)  # Thông dải 2.5-6Hz
h_high = signal.firwin(numtaps, 8/nyq, pass_zero=False)  # Thông cao 8Hz

# Hàm lưu thông số của bộ lọc
def save_filter_info(h, name, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        # Thông tin chung
        f.write(f"Thông số của bộ lọc {name}\n")
        f.write("="*50 + "\n\n")
        
        # Thông số cơ bản
        f.write(f"Số hệ số (bậc của bộ lọc): {len(h)-1}\n")
        f.write(f"Tần số lấy mẫu: {fs} Hz\n")
        f.write(f"Tần số Nyquist: {nyq} Hz\n\n")
        
        # Đáp ứng xung h(k)
        f.write("Đáp ứng xung h(k):\n")
        f.write("-"*30 + "\n")
        for k in range(len(h)):
            f.write(f"h({k:3d}) = {h[k]:15.10f}\n")
        
        # Tính đáp ứng tần số
        w, H = signal.freqz(h, worN=8000)
        freq = w * fs / (2*np.pi)
        mag = np.abs(H)
        phase = np.unwrap(np.angle(H))
        
        # Lưu đáp ứng tần số H(z)
        f.write("\nĐáp ứng tần số H(z):\n")
        f.write("-"*30 + "\n")
        f.write("Tần số(Hz)  |H(z)|(dB)    Pha(độ)\n")
        f.write("-"*50 + "\n")
        for i in range(0, len(freq), 10):  # Lưu mỗi điểm thứ 10 để file không quá lớn
            f.write(f"{freq[i]:10.3f} {20*np.log10(mag[i]):12.3f} {phase[i]*180/np.pi:12.3f}\n")
        
        # Các thông số quan trọng
        f.write("\nCác thông số quan trọng:\n")
        f.write("-"*30 + "\n")
        f.write(f"Độ lợi lớn nhất (dB): {20*np.log10(np.max(mag)):.2f}\n")
        f.write(f"Độ suy giảm lớn nhất (dB): {20*np.log10(np.min(mag)):.2f}\n")
        
        # Tìm tần số cắt (-3dB points)
        cutoff_mask = np.where(20*np.log10(mag) >= -3)[0]
        if len(cutoff_mask) > 0:
            f_cutoff = w[cutoff_mask] * fs / (2*np.pi)
            f.write(f"Tần số cắt -3dB (Hz): {f_cutoff[0]:.2f} - {f_cutoff[-1]:.2f}\n")

# Lưu thông số của từng bộ lọc
save_filter_info(h_low, "Thông thấp", "filter_lowpass.txt")
save_filter_info(h_band, "Thông dải", "filter_bandpass.txt")
save_filter_info(h_high, "Thông cao", "filter_highpass.txt")

# Lưu các hệ số vào file CSV để dễ import vào Excel/MATLAB
np.savetxt('filter_coefficients.csv', 
           np.column_stack((np.arange(len(h_low)), h_low, h_band, h_high)),
           delimiter=',',
           header='k,h_low(k),h_band(k),h_high(k)',
           comments='',
           fmt=['%d', '%.10f', '%.10f', '%.10f'])

# Vẽ đáp ứng xung của các bộ lọc
fig_impulse = plt.figure(figsize=(15, 10))
fig_impulse.suptitle('Đáp ứng xung h(k) của các bộ lọc', fontsize=16)

# Đáp ứng xung của bộ lọc thông thấp
plt.subplot(311)
plt.stem(np.arange(len(h_low)), h_low, 'r', label='Thông thấp 3Hz', use_line_collection=True)
plt.grid(True)
plt.legend(loc='best')
plt.xlabel('k (mẫu)')
plt.ylabel('h(k)')
plt.title('Đáp ứng xung của bộ lọc thông thấp')

# Đáp ứng xung của bộ lọc thông dải
plt.subplot(312)
plt.stem(np.arange(len(h_band)), h_band, 'g', label='Thông dải 2.5-6Hz', use_line_collection=True)
plt.grid(True)
plt.legend(loc='best')
plt.xlabel('k (mẫu)')
plt.ylabel('h(k)')
plt.title('Đáp ứng xung của bộ lọc thông dải')

# Đáp ứng xung của bộ lọc thông cao
plt.subplot(313)
plt.stem(np.arange(len(h_high)), h_high, 'b', label='Thông cao 8Hz', use_line_collection=True)
plt.grid(True)
plt.legend(loc='best')
plt.xlabel('k (mẫu)')
plt.ylabel('h(k)')
plt.title('Đáp ứng xung của bộ lọc thông cao')

plt.tight_layout()

# Vẽ đáp ứng tần số H(z) của các bộ lọc
fig_hz = plt.figure(figsize=(15, 10))
fig_hz.suptitle('Đáp ứng tần số H(z) của các bộ lọc', fontsize=16)

# Tính H(z) cho các bộ lọc
w, h_low_z = signal.freqz(h_low, worN=8000)
w, h_band_z = signal.freqz(h_band, worN=8000)
w, h_high_z = signal.freqz(h_high, worN=8000)
freq_hz = w * fs / (2*np.pi)

# Biên độ của H(z)
plt.subplot(211)
plt.plot(freq_hz, 20*np.log10(np.abs(h_low_z)), 'r-', label='Thông thấp 3Hz')
plt.plot(freq_hz, 20*np.log10(np.abs(h_band_z)), 'g-', label='Thông dải 2.5-6Hz')
plt.plot(freq_hz, 20*np.log10(np.abs(h_high_z)), 'b-', label='Thông cao 8Hz')
plt.grid(True)
plt.legend(loc='best')
plt.xlabel('Tần số (Hz)')
plt.ylabel('|H(z)| (dB)')
plt.title('Biên độ của hàm truyền đạt H(z)')
plt.xlim(0, 15)
plt.ylim(-80, 5)

# Pha của H(z)
plt.subplot(212)
plt.plot(freq_hz, np.unwrap(np.angle(h_low_z))*180/np.pi, 'r-', label='Thông thấp 3Hz')
plt.plot(freq_hz, np.unwrap(np.angle(h_band_z))*180/np.pi, 'g-', label='Thông dải 2.5-6Hz')
plt.plot(freq_hz, np.unwrap(np.angle(h_high_z))*180/np.pi, 'b-', label='Thông cao 8Hz')
plt.grid(True)
plt.legend(loc='best')
plt.xlabel('Tần số (Hz)')
plt.ylabel('∠H(z) (độ)')
plt.title('Pha của hàm truyền đạt H(z)')
plt.xlim(0, 15)

plt.tight_layout()

# Lưu thêm các hình mới
fig_impulse.savefig('impulse_response.png', dpi=300, bbox_inches='tight')
fig_hz.savefig('transfer_function.png', dpi=300, bbox_inches='tight')

# Lọc tín hiệu
y_low = signal.lfilter(h_low, 1.0, x)
y_band = signal.lfilter(h_band, 1.0, x)
y_high = signal.lfilter(h_high, 1.0, x)

# Tính đáp ứng tần số của các bộ lọc
w_low, h_low_freq = signal.freqz(h_low, worN=800)
w_band, h_band_freq = signal.freqz(h_band, worN=800)
w_high, h_high_freq = signal.freqz(h_high, worN=800)

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