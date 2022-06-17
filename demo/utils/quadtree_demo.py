import pymorton as pm

mortoncode1 = pm.interleave3(806, 401, 10) # 188786794
mortoncode2 = pm.interleave3(807, 401, 10) # 188786795
mortoncode3 = pm.interleave3(1613, 803, 11) # 436537975
mortoncode4 = pm.interleave3(1614, 803, 10) # 436537978



print(pm.interleave2(255, 255)) # 436537972
# print(pm.interleave(254, 25)) # 436537972
# print(pm.interleave(262143, 262143)) # 436537972
print((pm.deinterleave2(867)))

# print(mortoncode1)
# print(mortoncode2)
# print(mortoncode3)
# print(mortoncode4)