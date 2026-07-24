str=input("enter your string")
count=0
for ch in str:
    if ch in "aeiouAEIOU":
        count+=1
print("the count of vowels is",count)
