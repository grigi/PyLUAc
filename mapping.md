# Mapping from Python to LUA

<table>
<thead><tr><th>Statement</th><th>Python</th><th>LUA</th></tr></thead>
<tbody>
<tr>
<th>for range(size)</th>
<td><pre>
for A in range(10):
    {block}
</pre></td>
<td><pre>
for A = 0, 9 do
    {block} 
end
</pre></td>
</tr>
<tr>
<th>for range(start, end)</th>
<td><pre>
for A in range(1, 10):
    {block}
</pre></td>
<td><pre>
for A = 1, 10 do
    {block} 
end
</pre></td>
</tr>
<tr>
<th>for range(start, end, increment)</th>
<td><pre>
for A in range(1, 10, 2):
    {block}
</pre></td>
<td><pre>
for A = 1, 10, 2 do
    {block} 
end
</pre></td>
</tr>
<tr>
<th>for iterator</th>
<td><pre>
for A in [iterable]:
    {block}
</pre></td>
<td><pre>
# If iterable is static with no Nulls?
for A in [iterable] do
    {block} 
end
# Else, a while or repeat statement?
</pre></td>
</tr>
<tr>
<th>while</th>
<td><pre>
while [expression]:
    {block}
</pre></td>
<td><pre>
while [expression] do
    {block} 
end
</pre></td>
</tr>
<tr>
<th>if</th>
<td><pre>
if [expression]:
    {block} 
elif [expression]:
    {block} 
else:
    {block} 
</pre></td>
<td><pre>
if [expression] then 
    {block} 
elseif [expression] then
    {block} 
else 
    {block} 
end
</pre></td>
</tr>
</tbody>
</table>


