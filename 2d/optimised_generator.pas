
label l1,l2,l3;
var 
m,n,a,b,c,l,h_b,h_c,h_l,g,t,r:int64;
i,j:integer;
s:array[1..2000,1..5]of integer;
f:text;
function evk(a,b:integer):integer;
  var x,y,p,k:integer;
  begin
  if(a = 0)then
    x:=n
  else
    x:=a;
  if(b = 0)then
    y:=n
  else
    y:=b;
  while (y > 0) do begin
  if(x > y)then
    begin
    p:=y;
    k:=x;
    end
  else
    begin
    k:=y;
    p:=x;
    end;
  x:=y;
  y:=k mod p;
  end;
  evk:=x;
  end;
begin
assign(f, 'steinhaus-input');
rewrite(f);
write('Max number of iterations:');
readln(n);
a:=0;
while a <= n do
begin
  a:=a + 8;  
  if(a mod 7 <> 0)then
    h_b:=7
  else
    h_b:=1;
  b:=0;
  
  while b <= n do
    begin
    l1:
    b:=b + h_b;
    if(b mod 8 = 0)then goto l1;
    if(h_b = 1)and(b mod 7 = 0)then goto l1;
    
    if(a mod 5 = 0)or(b mod 5 = 0)then
      h_c:=1
    else
      h_c:=5;
    c:=0;
    
    while c <= n do
      begin
      l2:
      c:=c + h_c;
      if(c mod 7 = 0)or(c mod 8 = 0)then
        goto l2;
      if(h_c = 1)and(c mod 5 = 0)then
        goto l2;
      if(a mod 3 <> 0)and(b mod 3 <> 0)and(c mod 3 <> 0)then
        h_l:=3
      else
        h_l:=1;
      l:=0;
        while l <= n do
          begin
          l:=l + h_l;
          s[t+1,1]:=a;
          s[t+1,2]:=b;
          s[t+1,3]:=c;
          s[t+1,4]:=l;
          for i:=1 to 4 do
            for j:=1 to i do
              if(s[i,j+1] < s[i,j])then
                begin
                g:=s[t+1,j+1];
                s[t+1,j+1]:=s[i,j];
                s[t+1,j]:=g;
                end;
          r:=0;
          for i:=1 to t do
              if(s[i,1] = s[t+1,1])and(s[i,2] = s[t+1,2])and(s[i,3] = s[t+1,3])and(s[i,4] = s[t+1,4])then
                r:=1;
          writeln(a,' ',b,' ',c,' ',l);
          if(evk(evk(evk(a,b),c),l) = 1)and(r = 0)then
          if((a*a*a*a+b*b*b*b+c*c*c*c+l*l*l*l) = ((a*a*l*l+a*a*b*b+b*b*l*l+a*a*c*c+b*b*c*c+c*c*l*l)))then
             begin
             writeln(f,a,' ',b,' ',c,' ',l);
             writeln('!!!  ',a,' ',b,' ',c,' ',l);
             t:=t+1;
             end;
        end;
      end;
    end;
end;
close(f);
end.
