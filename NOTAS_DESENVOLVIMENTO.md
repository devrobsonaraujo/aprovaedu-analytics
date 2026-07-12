# Notas do Desenvolvimento

Registro pessoal de descobertas e decisões ao longo do desafio.

## Descobertas iniciais (primeira exploração dos dados)

- Percebi que as abas tinham tamanhos diferentes do indicado no Resumo
- A aba Presenças_Aulas tinha só 500 linhas, mas o resumo falava em 74997
- Isso mudou completamente minha estratégia, em resumo não posso calcular taxas exatas

## Problemas encontrados

- Datas em formatos mistos deram trabalho
- Universidades escritas de 3 formas diferentes (minúscula, maiúscula, abreviado)
- 15 registros duplicados em Aprovações, usei a coluna "chamada" pra identificar

## Dúvidas que tive:

- Como definir "aprovado" se não tem tabela de reprovados? Então decidi que quem não aparece em Aprovações = não aprovado.
- Atrasado conta como presença? Considerei que sim, pois é melhor que ausente
- Por fim, seriam questionamentos que iria fazer ao cliente, como é um teste e o tempo bem corrido para mim, acabei por levar essas considerações nos questionamentos que tive.
