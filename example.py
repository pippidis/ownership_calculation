from company_ownership import Company

c = Company(name='Example Company', original_owner='Johannes')
print(c)

c.add_owner('Johannes Clone', 100)
print(c)

c.transfer_stocks('Johannes', 'Johannes Clone', 10)
print(c)