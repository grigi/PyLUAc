# Mapping from Python to LUA


## FOR statement
### range(size)
```
for A in range(10):
    {block} 

for A = 0, 9 do
    {block} 
end
```

### range(start, end)
```
for A in range(1,10):
    {block} 

for A = 1, 10 do
    {block} 
end
```

### range(start, end, increment)
```
for A in range(0,10,2):
    {block} 

for A = 0, 10, 2 do
    {block} 
end
```

### iterator
```
for A, B in [explist]:
    {block} 

for A, B in [explist] do
    {block}
end
```

## WHILE statement
```
while [expression]:
    {block} 

while [expression] do
    {block} 
end
```

## IF statement
```
if [expression]:
    {block} 
elif [expression]:
    {block} 
else:
    {block} 

if [expression] then 
    {block} 
elseif [expression] then
    {block} 
else 
    {block} 
end
```
