# PORTFOLIO SIZE ENCODING AUDIT

Portfolio size inequality sum(x_i) <= K is transformed to equality sum(x_i) + s = K via binary exponential slack s = sum(2^b * s_b) and squared penalty P_size * (sum(x_i) + s - K)^2.
