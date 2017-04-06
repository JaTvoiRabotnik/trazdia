import collector

# Test script. This should get all docs from edition 1772.
ediParam = 1772
materias = collector.getMetadata.getedition(ediParam, False)
for materia in materias:
    matParam = materia['matId']
    print('Outputting tokens to ../tokens/' + str(ediParam) + '-' + str(matParam) + '.txt')
    # TODO we should be outputting to a place given as a parameter, not hardcoded.
    f = open('../tokens/' + str(ediParam) + '-' + str(matParam) + '.txt', 'w')
    f.write(collector.getDocument.extract_tokens(materia))
    f.close()
