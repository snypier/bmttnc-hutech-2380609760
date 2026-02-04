print("Nhập văn bản")
lines = []
while True:
    line = input()
    if line.lower() == 'done':
        break
    lines.append(line)
print("Các văn bản khi chuyển in hoa")
for line in lines:
    print(line.upper())    
