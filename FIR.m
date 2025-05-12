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

% Tạo các bộ lọc
h_low = fir1(numtaps-1, 3/nyq, 'low');  % Thông thấp 3Hz
h_band = fir1(numtaps-1, [2.5 6]/nyq, 'bandpass');  % Thông dải 2.5-6Hz
h_high = fir1(numtaps-1, 8/nyq, 'high');  % Thông cao 8Hz

% Lọc tín hiệu
y_low = filter(h_low, 1, x);
y_band = filter(h_band, 1, x);
y_high = filter(h_high, 1, x);

% Hàm lưu thông số của bộ lọc
function save_filter_info(h, name, filename)
    % Mở file để ghi
    fid = fopen(filename, 'w');
    
    % Thông tin chung
    fprintf(fid, 'Thông số của bộ lọc %s\n', name);
    fprintf(fid, '%s\n\n', repmat('=', 1, 50));
    
    % Thông số cơ bản
    fprintf(fid, 'Số hệ số (bậc của bộ lọc): %d\n', length(h)-1);
    fprintf(fid, 'Tần số lấy mẫu: %d Hz\n', fs);
    fprintf(fid, 'Tần số Nyquist: %d Hz\n\n', nyq);
    
    % Đáp ứng xung h(k)
    fprintf(fid, 'Đáp ứng xung h(k):\n');
    fprintf(fid, '%s\n', repmat('-', 1, 30));
    for k = 1:length(h)
        fprintf(fid, 'h(%3d) = %15.10f\n', k-1, h(k));
    end
    
    % Tính đáp ứng tần số
    [H, w] = freqz(h, 1, 800);
    freq = w * fs / (2*pi);
    mag = abs(H);
    phase = unwrap(angle(H));
    
    % Lưu đáp ứng tần số H(z)
    fprintf(fid, '\nĐáp ứng tần số H(z):\n');
    fprintf(fid, '%s\n', repmat('-', 1, 30));
    fprintf(fid, 'Tần số(Hz)  |H(z)|(dB)    Pha(độ)\n');
    fprintf(fid, '%s\n', repmat('-', 1, 50));
    for i = 1:10:length(freq)
        fprintf(fid, '%10.3f %12.3f %12.3f\n', freq(i), ...
                20*log10(mag(i)), phase(i)*180/pi);
    end
    
    % Các thông số quan trọng
    fprintf(fid, '\nCác thông số quan trọng:\n');
    fprintf(fid, '%s\n', repmat('-', 1, 30));
    fprintf(fid, 'Độ lợi lớn nhất (dB): %.2f\n', 20*log10(max(mag)));
    fprintf(fid, 'Độ suy giảm lớn nhất (dB): %.2f\n', 20*log10(min(mag)));
    
    % Tìm tần số cắt (-3dB points)
    cutoff_mask = find(20*log10(mag) >= -3);
    if ~isempty(cutoff_mask)
        f_cutoff = w(cutoff_mask) * fs / (2*pi);
        fprintf(fid, 'Tần số cắt -3dB (Hz): %.2f - %.2f\n', ...
                f_cutoff(1), f_cutoff(end));
    end
    
    fclose(fid);
end

% Lưu thông số của từng bộ lọc
save_filter_info(h_low, 'Thông thấp', 'filter_lowpass.txt');
save_filter_info(h_band, 'Thông dải', 'filter_bandpass.txt');
save_filter_info(h_high, 'Thông cao', 'filter_highpass.txt');

% Lưu các hệ số vào file CSV
coeff_table = [(0:length(h_low)-1)' h_low' h_band' h_high'];
fid = fopen('filter_coefficients.csv', 'w');
fprintf(fid, 'k,h_low(k),h_band(k),h_high(k)\n');
fprintf(fid, '%d,%.10f,%.10f,%.10f\n', coeff_table');
fclose(fid);

% Vẽ tín hiệu trong miền thời gian (2x2)
figure('Position', [100 100 1000 800]);
sgtitle('Tín hiệu trong miền thời gian', 'FontSize', 16);

% Tín hiệu gốc
subplot(221);
plot(t, x, 'k-', 'LineWidth', 1.5);
grid on;
legend('Tín hiệu gốc', 'Location', 'best');
xlabel('Thời gian (s)');
ylabel('Biên độ');
title('Tín hiệu gốc');

% Tín hiệu sau lọc thông thấp
subplot(222);
plot(t, x, 'k--', t, y_low, 'r-', 'LineWidth', 1.5);
grid on;
legend('Tín hiệu gốc', 'Sau lọc thông thấp 3Hz', 'Location', 'best');
xlabel('Thời gian (s)');
ylabel('Biên độ');
title('Tín hiệu sau lọc thông thấp');

% Tín hiệu sau lọc thông dải
subplot(223);
plot(t, x, 'k--', t, y_band, 'g-', 'LineWidth', 1.5);
grid on;
legend('Tín hiệu gốc', 'Sau lọc thông dải 2.5-6Hz', 'Location', 'best');
xlabel('Thời gian (s)');
ylabel('Biên độ');
title('Tín hiệu sau lọc thông dải');

% Tín hiệu sau lọc thông cao
subplot(224);
plot(t, x, 'k--', t, y_high, 'b-', 'LineWidth', 1.5);
grid on;
legend('Tín hiệu gốc', 'Sau lọc thông cao 8Hz', 'Location', 'best');
xlabel('Thời gian (s)');
ylabel('Biên độ');
title('Tín hiệu sau lọc thông cao');

% Vẽ đáp ứng tần số của bộ lọc
figure('Position', [100 100 1000 800]);
sgtitle('Đáp ứng tần số của bộ lọc', 'FontSize', 16);

% Tính H(z) cho các bộ lọc
[h_low_z, w] = freqz(h_low, 1, 800);
[h_band_z, ~] = freqz(h_band, 1, 800);
[h_high_z, ~] = freqz(h_high, 1, 800);
freq_hz = w * fs / (2*pi);

% Biên độ của H(z)
subplot(211);
plot(freq_hz, 20*log10(abs(h_low_z)), 'r-', ...
     freq_hz, 20*log10(abs(h_band_z)), 'g-', ...
     freq_hz, 20*log10(abs(h_high_z)), 'b-', ...
     'LineWidth', 1.5);
grid on;
legend('Thông thấp 3Hz', 'Thông dải 2.5-6Hz', 'Thông cao 8Hz', ...
       'Location', 'best');
xlabel('Tần số (Hz)');
ylabel('|H(z)| (dB)');
title('Biên độ của hàm truyền đạt H(z)');
xlim([0 15]);
ylim([-80 5]);

% Pha của H(z)
subplot(212);
plot(freq_hz, unwrap(angle(h_low_z))*180/pi, 'r-', ...
     freq_hz, unwrap(angle(h_band_z))*180/pi, 'g-', ...
     freq_hz, unwrap(angle(h_high_z))*180/pi, 'b-', ...
     'LineWidth', 1.5);
grid on;
legend('Thông thấp 3Hz', 'Thông dải 2.5-6Hz', 'Thông cao 8Hz', ...
       'Location', 'best');
xlabel('Tần số (Hz)');
ylabel('∠H(z) (độ)');
title('Pha của hàm truyền đạt H(z)');
xlim([0 15]);

% Vẽ đáp ứng xung của các bộ lọc
figure('Position', [100 100 1000 800]);
sgtitle('Đáp ứng xung h(k) của các bộ lọc', 'FontSize', 16);

% Đáp ứng xung của bộ lọc thông thấp
subplot(311);
stem(0:length(h_low)-1, h_low, 'r');
grid on;
legend('Thông thấp 3Hz', 'Location', 'best');
xlabel('k (mẫu)');
ylabel('h(k)');
title('Đáp ứng xung của bộ lọc thông thấp');

% Đáp ứng xung của bộ lọc thông dải
subplot(312);
stem(0:length(h_band)-1, h_band, 'g');
grid on;
legend('Thông dải 2.5-6Hz', 'Location', 'best');
xlabel('k (mẫu)');
ylabel('h(k)');
title('Đáp ứng xung của bộ lọc thông dải');

% Đáp ứng xung của bộ lọc thông cao
subplot(313);
stem(0:length(h_high)-1, h_high, 'b');
grid on;
legend('Thông cao 8Hz', 'Location', 'best');
xlabel('k (mẫu)');
ylabel('h(k)');
title('Đáp ứng xung của bộ lọc thông cao');

% Lưu các hình
saveas(gcf, 'impulse_response.png');
saveas(gcf, 'transfer_function.png');
saveas(gcf, 'time_domain_signals.png'); 