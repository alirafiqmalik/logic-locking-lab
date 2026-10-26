module top(a, b, y);
input a;
input b;
output y;
AND_g g0 ( .A(a), .B(b), .Y(y) );
endmodule
