% Các thông số
fs = 100;  % Tần số lấy mẫu (Hz)
t = 0:1/fs:2;  % Thời gian từ 0-2s

% Tạo tín hiệu đầu vào với 4 tần số khác nhau
f = [1 3 5 10];  % Các tần số (Hz)
A = [1 0.7 0.5 0.3];  % Biên độ tương ứng
x = A(1)*sin(2*pi*f(1)*t) + A(2)*sin(2*pi*f(2)*t) + ...
    A(3)*sin(2*pi*f(3)*t) + A(4)*sin(2*pi*f(4)*t);

% Thiết kế các bộ lọc FIR
nyq = fs/2;  % Tần số Nyquist
numtaps = 101;  % Số hệ số của bộ lọc

% Tạo bộ lọc thông thấp (cutoff = 3Hz)
h_low = fir1(numtaps-1, 2/nyq, 'low');

% Tạo bộ lọc thông dải (2.5-6Hz)
h_band = fir1(numtaps-1, [2.5 6]/nyq, 'bandpass');

% Tạo bộ lọc thông cao (8Hz)
h_high = fir1(numtaps-1, 8/nyq, 'high');

% Lọc tín hiệu
y_low = filter(h_low, 1, x);
y_band = filter(h_band, 1, x);
y_high = filter(h_high, 1, x);

% Tính phổ tần số
NFFT = length(t);
freq = linspace(0, fs/2, NFFT/2);
f_x = abs(fft(x, NFFT));
f_low = abs(fft(y_low, NFFT));
f_band = abs(fft(y_band, NFFT));
f_high = abs(fft(y_high, NFFT));

% Chuẩn hóa phổ và lấy nửa phổ dương
f_x = f_x(1:NFFT/2)/NFFT;
f_low = f_low(1:NFFT/2)/NFFT;
f_band = f_band(1:NFFT/2)/NFFT;
f_high = f_high(1:NFFT/2)/NFFT;

% Vẽ đồ thị
figure('Position', [100 100 1200 800]);

% Đồ thị tín hiệu thời gian
subplot(2,2,1);
plot(t, x, 'k-', 'LineWidth', 1.5, 'DisplayName', 'Tín hiệu gốc');
grid on;
legend('Location', 'best');
xlabel('Thời gian (s)');
ylabel('Biên độ');
title('Tín hiệu gốc trong miền thời gian');

% Đồ thị sau lọc thông thấp
subplot(2,2,2);
plot(t, x, 'k--', 'DisplayName', 'Tín hiệu gốc');
hold on;
plot(t, y_low, 'r-', 'LineWidth', 1.5, 'DisplayName', 'Lọc thông thấp 3Hz');
grid on;
legend('Location', 'best');
xlabel('Thời gian (s)');
ylabel('Biên độ');
title('Tín hiệu sau lọc thông thấp');

% Đồ thị sau lọc thông dải
subplot(2,2,3);
plot(t, x, 'k--', 'DisplayName', 'Tín hiệu gốc');
hold on;
plot(t, y_band, 'g-', 'LineWidth', 1.5, 'DisplayName', 'Lọc thông dải 2.5-6Hz');
grid on;
legend('Location', 'best');
xlabel('Thời gian (s)');
ylabel('Biên độ');
title('Tín hiệu sau lọc thông dải');

% Đồ thị sau lọc thông cao
subplot(2,2,4);
plot(t, x, 'k--', 'DisplayName', 'Tín hiệu gốc');
hold on;
plot(t, y_high, 'b-', 'LineWidth', 1.5, 'DisplayName', 'Lọc thông cao 8Hz');
grid on;
legend('Location', 'best');
xlabel('Thời gian (s)');
ylabel('Biên độ');
title('Tín hiệu sau lọc thông cao');

% Tạo figure mới cho phổ tần số
figure('Position', [100 100 1200 800]);

% Đồ thị phổ tần số của tất cả các tín hiệu
plot(freq, f_x, 'k-', 'LineWidth', 1.5, 'DisplayName', 'Tín hiệu gốc');
hold on;
plot(freq, f_low, 'r-', 'LineWidth', 1.5, 'DisplayName', 'Sau lọc thông thấp');
plot(freq, f_band, 'g-', 'LineWidth', 1.5, 'DisplayName', 'Sau lọc thông dải');
plot(freq, f_high, 'b-', 'LineWidth', 1.5, 'DisplayName', 'Sau lọc thông cao');
grid on;
legend('Location', 'best');
xlabel('Tần số (Hz)');
ylabel('Biên độ');
title('Phổ tần số của các tín hiệu');

% Giới hạn trục x để dễ quan sát
xlim([0 15]);

% Điều chỉnh màu nền
set(gcf, 'Color', 'w');