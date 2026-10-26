module top(a, b, keyinput0, y);
input a;
input b;
input keyinput0;
output y;
wire n;
AND_g g0 ( .A(a), .B(b), .Y(n) );
XOR_g g1 ( .A(n), .B(keyinput0), .Y(y) );
endmodule
