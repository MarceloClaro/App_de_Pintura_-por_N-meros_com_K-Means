# Importando todas as coisas necessárias para o nosso programa funcionar.
# Esses são como os blocos de construção que vamos usar para fazer o nosso programa.

import numpy as np  # Esta é uma ferramenta para lidar com listas de números.
from sklearn.cluster import KMeans  # Essa é uma ferramenta que nos ajuda a encontrar grupos de coisas.
from sklearn.utils import shuffle  # Isso nos ajuda a misturar coisas.
import cv2  # Esta é uma ferramenta para trabalhar com imagens.
import streamlit as st  # Isso é o que nos permite criar a interface do nosso programa.
from PIL import Image  # Outra ferramenta para trabalhar com imagens.
import io  # Essa é uma ferramenta que nos ajuda a lidar com arquivos e dados.
import base64  # Essa é uma ferramenta que nos ajuda a converter dados.

# Lista de cores junguianas ampliada
cores_junguianas = {
    '1': {
        'cor': 'Preto',
        'rgb': (0, 0, 0),
        'anima_animus': 'A cor preta representa a sombra do inconsciente, simbolizando os aspectos desconhecidos e reprimidos de uma pessoa.',
        'sombra': 'A cor preta é a própria sombra, representando os instintos primordiais e os aspectos ocultos da personalidade.',
        'personalidade': 'A cor preta pode indicar uma personalidade enigmática, poderosa e misteriosa.',
        'diagnostico': 'O uso excessivo da cor preta pode indicar uma tendência à negatividade, depressão ou repressão emocional.'
    },
    '2': {
        'cor': 'Preto carvão',
        'rgb': (10, 10, 10),
        'anima_animus': 'O preto carvão simboliza a sombra feminina do inconsciente, representando os aspectos desconhecidos e reprimidos da feminilidade.',
        'sombra': 'O preto carvão é a própria sombra feminina, representando os instintos primordiais e os aspectos ocultos da feminilidade.',
        'personalidade': 'A cor preto carvão pode indicar uma personalidade poderosa, misteriosa e enigmática com uma forte presença feminina.',
        'diagnostico': 'O uso excessivo da cor preto carvão pode indicar uma tendência à negatividade, depressão ou repressão emocional na expressão feminina.'
    },
    '3': {
        'cor': 'Cinza escuro',
        'rgb': (17, 17, 17),
        'anima_animus': 'O cinza escuro representa a parte sombria e desconhecida do inconsciente, relacionada aos aspectos reprimidos e negligenciados da personalidade.',
        'sombra': 'O cinza escuro simboliza a sombra interior, representando a reserva de energia não utilizada e os aspectos ocultos da personalidade.',
        'personalidade': 'A cor cinza escuro pode indicar uma personalidade reservada, misteriosa e com profundidade interior.',
        'diagnostico': 'O uso excessivo da cor cinza escuro pode indicar uma tendência a se esconder, reprimir emoções ou evitar o autoconhecimento.'
    },
    '4': {
        'cor': 'Cinza ardósia',
        'rgb': (47, 79, 79),
        'anima_animus': 'O cinza ardósia representa a sombra feminina do inconsciente, relacionada aos aspectos reprimidos e negligenciados da feminilidade.',
        'sombra': 'O cinza ardósia é a própria sombra feminina, representando a reserva de energia não utilizada e os aspectos ocultos da feminilidade.',
        'personalidade': 'A cor cinza ardósia pode indicar uma personalidade reservada, misteriosa e com uma forte presença feminina.',
        'diagnostico': 'O uso excessivo da cor cinza ardósia pode indicar uma tendência a se esconder, reprimir emoções ou evitar o autoconhecimento na expressão feminina.'
    },
    '5': {
        'cor': 'Branco',
        'rgb': (255, 255, 255),
        'anima_animus': 'O branco representa a luz, a pureza e a clareza.',
        'sombra': 'O branco é a própria luz, representando a falta de sombra e a transparência.',
        'personalidade': 'A cor branca pode indicar uma personalidade pura, inocente e clara.',
        'diagnostico': 'O uso excessivo da cor branca pode indicar uma tendência à neutralidade, falta de personalidade ou falta de profundidade emocional.'
    },
    '6': {
        'cor': 'Azul claro',
        'rgb': (173, 216, 230),
        'anima_animus': 'O azul claro representa a tranquilidade, a serenidade e a paz.',
        'sombra': 'O azul claro é a sombra da passividade, da falta de iniciativa e da indiferença emocional.',
        'personalidade': 'A cor azul claro pode indicar uma personalidade tranquila, serena e em busca de paz interior.',
        'diagnostico': 'O uso excessivo da cor azul claro pode indicar uma tendência à passividade, falta de iniciativa ou indiferença emocional.'
    },
    '7': {
        'cor': 'Verde claro',
        'rgb': (144, 238, 144),
        'anima_animus': 'O verde claro representa a esperança, o crescimento e a renovação.',
        'sombra': 'O verde claro é a sombra da inveja, da ganância e da falta de maturidade emocional.',
        'personalidade': 'A cor verde claro pode indicar uma personalidade esperançosa, em constante crescimento e busca de renovação.',
        'diagnostico': 'O uso excessivo da cor verde claro pode indicar uma tendência à inveja, ganância ou falta de maturidade emocional.'
    },
    '8': {
        'cor': 'Vermelho',
        'rgb': (255, 0, 0),
        'anima_animus': 'O vermelho representa a paixão, a energia e a ação.',
        'sombra': 'O vermelho é a sombra da raiva, da agressividade e da impulsividade.',
        'personalidade': 'A cor vermelha pode indicar uma personalidade apaixonada, energética e propensa à ação.',
        'diagnostico': 'O uso excessivo da cor vermelha pode indicar uma tendência à raiva, agressividade ou impulsividade.'
    },
    '9': {
        'cor': 'Amarelo',
        'rgb': (255, 255, 0),
        'anima_animus': 'O amarelo representa a alegria, a felicidade e a positividade.',
        'sombra': 'O amarelo é a sombra do medo, da insegurança e da ansiedade.',
        'personalidade': 'A cor amarela pode indicar uma personalidade alegre, feliz e positiva.',
        'diagnostico': 'O uso excessivo da cor amarela pode indicar uma tendência ao medo, insegurança ou ansiedade.'
    },
    '10': {
        'cor': 'Laranja',
        'rgb': (255, 165, 0),
        'anima_animus': 'O laranja representa a criatividade, a energia e a confiança.',
        'sombra': 'O laranja é a sombra da arrogância, da impulsividade e do excesso de confiança.',
        'personalidade': 'A cor laranja pode indicar uma personalidade criativa, enérgica e confiante.',
        'diagnostico': 'O uso excessivo da cor laranja pode indicar uma tendência à arrogância, impulsividade ou excesso de confiança.'
    },
    '11': {
        'cor': 'Rosa',
        'rgb': (255, 192, 203),
        'anima_animus': 'O rosa representa o amor, a delicadeza e a compaixão.',
        'sombra': 'O rosa é a sombra da dependência emocional, da sensibilidade excessiva e da carência afetiva.',
        'personalidade': 'A cor rosa pode indicar uma personalidade amorosa, delicada e compassiva.',
        'diagnostico': 'O uso excessivo da cor rosa pode indicar uma tendência à dependência emocional, sensibilidade excessiva ou carência afetiva.'
    },
    '12': {
        'cor': 'Roxo',
        'rgb': (128, 0, 128),
        'anima_animus': 'O roxo representa a espiritualidade, a intuição e o mistério.',
        'sombra': 'O roxo é a sombra da obsessão, da manipulação e da falta de clareza mental.',
        'personalidade': 'A cor roxa pode indicar uma personalidade espiritual, intuitiva e misteriosa.',
        'diagnostico': 'O uso excessivo da cor roxa pode indicar uma tendência à obsessão, manipulação ou falta de clareza mental.'
    },
    '13': {
        'cor': 'Marrom',
        'rgb': (139, 69, 19),
        'anima_animus': 'O marrom representa a estabilidade, a segurança e a confiabilidade.',
        'sombra': 'O marrom é a sombra da teimosia, da resistência à mudança e da rigidez mental.',
        'personalidade': 'A cor marrom pode indicar uma personalidade estável, segura e confiável.',
        'diagnostico': 'O uso excessivo da cor marrom pode indicar uma tendência à teimosia, resistência à mudança ou rigidez mental.'
    },
    '14': {
        'cor': 'Verde',
        'rgb': (0, 128, 0),
        'anima_animus': 'O verde representa a harmonia, o equilíbrio e a saúde.',
        'sombra': 'O verde é a sombra da inveja, da ganância e do desequilíbrio emocional.',
        'personalidade': 'A cor verde pode indicar uma personalidade harmoniosa, equilibrada e saudável.',
        'diagnostico': 'O uso excessivo da cor verde pode indicar uma tendência à inveja, ganância ou desequilíbrio emocional.'
    },
    '15': {
        'cor': 'Azul',
        'rgb': (0, 0, 255),
        'anima_animus': 'O azul representa a calma, a confiança e a comunicação.',
        'sombra': 'O azul é a sombra da frieza emocional, da falta de expressão e da falta de empatia.',
        'personalidade': 'A cor azul pode indicar uma personalidade calma, confiante e comunicativa.',
        'diagnostico': 'O uso excessivo da cor azul pode indicar uma tendência à frieza emocional, falta de expressão ou falta de empatia.'
    },
    '16': {
        'cor': 'Ciano',
        'rgb': (0, 255, 255),
        'anima_animus': 'O ciano representa a criatividade, a intuição e a clareza mental.',
        'sombra': 'O ciano é a sombra da instabilidade emocional, da confusão mental e da falta de foco.',
        'personalidade': 'A cor ciano pode indicar uma personalidade criativa, intuitiva e mentalmente clara.',
        'diagnostico': 'O uso excessivo da cor ciano pode indicar uma tendência à instabilidade emocional, confusão mental ou falta de foco.'
    },
    '17': {
        'cor': 'Magenta',
        'rgb': (255, 0, 255),
        'anima_animus': 'O magenta representa a paixão, a sensualidade e a expressão emocional.',
        'sombra': 'O magenta é a sombra do excesso emocional, da impulsividade e da falta de controle.',
        'personalidade': 'A cor magenta pode indicar uma personalidade apaixonada, sensual e expressiva emocionalmente.',
        'diagnostico': 'O uso excessivo da cor magenta pode indicar uma tendência ao excesso emocional, impulsividade ou falta de controle.'
    },
    '18': {
        'cor': 'Violeta',
        'rgb': (238, 130, 238),
        'anima_animus': 'O violeta representa a espiritualidade, a intuição e a transmutação.',
        'sombra': 'O violeta é a sombra da arrogância espiritual, da falta de conexão com a realidade e da busca constante por escapismo.',
        'personalidade': 'A cor violeta pode indicar uma personalidade espiritual, intuitiva e em busca de transmutação.',
        'diagnostico': 'O uso excessivo da cor violeta pode indicar uma tendência à arrogância espiritual, falta de conexão com a realidade ou busca constante por escapismo.'
    },
    '19': {
        'cor': 'Dourado',
        'rgb': (255, 215, 0),
        'anima_animus': 'O dourado representa o poder, a riqueza e a sabedoria.',
        'sombra': 'O dourado é a sombra do egoísmo, da ganância e da busca pelo poder pelo poder.',
        'personalidade': 'A cor dourada pode indicar uma personalidade poderosa, rica e sábia.',
        'diagnostico': 'O uso excessivo da cor dourada pode indicar uma tendência ao egoísmo, ganância ou busca pelo poder pelo poder.'
    },
    '20': {
        'cor': 'Prata',
        'rgb': (192, 192, 192),
        'anima_animus': 'A cor prata representa a intuição, a emoção e a sensibilidade.',
        'sombra': 'A cor prata é a própria sombra da intuição, representando a falta de controle emocional e a suscetibilidade à influência externa.',
        'personalidade': 'A cor prata pode indicar uma personalidade intuitiva, emocional e sensível.',
        'diagnostico': 'O uso excessivo da cor prata pode indicar uma tendência à falta de controle emocional, suscetibilidade à influência externa ou falta de discernimento.'
    },
    '21': {
        'cor': 'Verde limão',
        'rgb': (50, 205, 50),
        'anima_animus': 'O verde limão representa a energia, a vitalidade e o otimismo.',
        'sombra': 'O verde limão é a sombra da impulsividade, da agitação e da superficialidade.',
        'personalidade': 'A cor verde limão pode indicar uma personalidade energética, vital e otimista.',
        'diagnostico': 'O uso excessivo da cor verde limão pode indicar uma tendência à impulsividade, agitação ou superficialidade.'
    },
    '22': {
        'cor': 'Turquesa',
        'rgb': (64, 224, 208),
        'anima_animus': 'O turquesa representa a comunicação, a calma e a clareza mental.',
        'sombra': 'O turquesa é a sombra da falta de comunicação, da timidez e da falta de clareza mental.',
        'personalidade': 'A cor turquesa pode indicar uma personalidade comunicativa, calma e mentalmente clara.',
        'diagnostico': 'O uso excessivo da cor turquesa pode indicar uma tendência à falta de comunicação, timidez ou falta de clareza mental.'
    },
    '23': {
        'cor': 'Marrom claro',
        'rgb': (205, 133, 63),
        'anima_animus': 'O marrom claro representa a estabilidade, a segurança e a confiabilidade.',
        'sombra': 'O marrom claro é a sombra da estagnação, da resistência à mudança e do apego ao passado.',
        'personalidade': 'A cor marrom claro pode indicar uma personalidade estável, segura e confiável.',
        'diagnostico': 'O uso excessivo da cor marrom claro pode indicar uma tendência à estagnação, resistência à mudança ou apego ao passado.'
    },
    '24': {
        'cor': 'Verde oliva',
        'rgb': (128, 128, 0),
        'anima_animus': 'O verde oliva representa a sabedoria, a paz interior e a resiliência.',
        'sombra': 'O verde oliva é a sombra da rigidez mental, da falta de adaptabilidade e da falta de equilíbrio emocional.',
        'personalidade': 'A cor verde oliva pode indicar uma personalidade sábia, em paz interior e resiliente.',
        'diagnostico': 'O uso excessivo da cor verde oliva pode indicar uma tendência à rigidez mental, falta de adaptabilidade ou falta de equilíbrio emocional.'
    },
    '25': {
        'cor': 'Cinza claro',
        'rgb': (211, 211, 211),
        'anima_animus': 'O cinza claro representa a neutralidade, a imparcialidade e a adaptabilidade.',
        'sombra': 'O cinza claro é a sombra da indecisão, da falta de identidade e da falta de assertividade.',
        'personalidade': 'A cor cinza claro pode indicar uma personalidade neutra, imparcial e adaptável.',
        'diagnostico': 'O uso excessivo da cor cinza claro pode indicar uma tendência à indecisão, falta de identidade ou falta de assertividade.'
    },
    '26': {
        'cor': 'Cinza chumbo',
        'rgb': (105, 105, 105),
        'anima_animus': 'O cinza chumbo representa a estabilidade, a solidez e a discrição.',
        'sombra': 'O cinza chumbo é a sombra da estagnação, da falta de criatividade e da falta de expressão emocional.',
        'personalidade': 'A cor cinza chumbo pode indicar uma personalidade estável, sólida e discreta.',
        'diagnostico': 'O uso excessivo da cor cinza chumbo pode indicar uma tendência à estagnação, falta de criatividade ou falta de expressão emocional.'
    },
    '27': {
        'cor': 'Azul celeste',
        'rgb': (135, 206, 235),
        'anima_animus': 'O azul celeste representa a liberdade, a expansão e a paz interior.',
        'sombra': 'O azul celeste é a sombra da irresponsabilidade, da falta de comprometimento e da fuga dos problemas.',
        'personalidade': 'A cor azul celeste pode indicar uma personalidade livre, expansiva e em paz interior.',
        'diagnostico': 'O uso excessivo da cor azul celeste pode indicar uma tendência à irresponsabilidade, falta de comprometimento ou fuga dos problemas.'
    },
    '28': {
        'cor': 'Verde água',
        'rgb': (127, 255, 212),
        'anima_animus': 'O verde água representa a cura, a harmonia e a renovação.',
        'sombra': 'O verde água é a sombra da falta de empatia, da insensibilidade emocional e da superficialidade nas relações.',
        'personalidade': 'A cor verde água pode indicar uma personalidade de cura, harmonia e renovação.',
        'diagnostico': 'O uso excessivo da cor verde água pode indicar uma tendência à falta de empatia, insensibilidade emocional ou superficialidade nas relações.'
    },
    '29': {
        'cor': 'Rosa claro',
        'rgb': (255, 182, 193),
        'anima_animus': 'O rosa claro representa a doçura, a delicadeza e a compreensão.',
        'sombra': 'O rosa claro é a sombra da ingenuidade, da dependência emocional e da falta de assertividade.',
        'personalidade': 'A cor rosa claro pode indicar uma personalidade doce, delicada e compreensiva.',
        'diagnostico': 'O uso excessivo da cor rosa claro pode indicar uma tendência à ingenuidade, dependência emocional ou falta de assertividade.'
    },
    '30': {
        'cor': 'Lilás',
        'rgb': (200, 162, 200),
        'anima_animus': 'O lilás representa a espiritualidade, a intuição e a transformação.',
        'sombra': 'O lilás é a sombra da manipulação, da falta de autoconsciência e da busca constante por significado.',
        'personalidade': 'A cor lilás pode indicar uma personalidade espiritual, intuitiva e em busca de transformação.',
        'diagnostico': 'O uso excessivo da cor lilás pode indicar uma tendência à manipulação, falta de autoconsciência ou busca constante por significado.'
    },
    '31': {
        'cor': 'Bege',
        'rgb': (245, 245, 220),
        'anima_animus': 'O bege representa a simplicidade, a modéstia e a estabilidade emocional.',
        'sombra': 'O bege é a sombra da falta de individualidade, da falta de ambição e da falta de emoções intensas.',
        'personalidade': 'A cor bege pode indicar uma personalidade simples, modesta e emocionalmente estável.',
        'diagnostico': 'O uso excessivo da cor bege pode indicar uma tendência à falta de individualidade, falta de ambição ou falta de emoções intensas.'
    },
    '32': {
        'cor': 'Azul marinho',
        'rgb': (0, 0, 128),
        'anima_animus': 'O azul marinho representa a profundidade emocional, a intuição e a sabedoria.',
        'sombra': 'O azul marinho é a sombra da depressão, da falta de clareza emocional e da rigidez mental.',
        'personalidade': 'A cor azul marinho pode indicar uma personalidade com profundidade emocional, intuitiva e sábia.',
        'diagnostico': 'O uso excessivo da cor azul marinho pode indicar uma tendência à depressão, falta de clareza emocional ou rigidez mental.'
    },
    '33': {
        'cor': 'Verde musgo',
        'rgb': (128, 128, 0),
        'anima_animus': 'O verde musgo representa a estabilidade, a segurança e a conexão com a natureza.',
        'sombra': 'O verde musgo é a sombra do conformismo, da resistência à mudança e do apego ao passado.',
        'personalidade': 'A cor verde musgo pode indicar uma personalidade estável, segura e conectada com a natureza.',
        'diagnostico': 'O uso excessivo da cor verde musgo pode indicar uma tendência ao conformismo, resistência à mudança ou apego ao passado.'
    },
    '34': {
        'cor': 'Cinza azulado',
        'rgb': (176, 196, 222),
        'anima_animus': 'O cinza azulado representa a harmonia, a paz e a serenidade.',
        'sombra': 'O cinza azulado é a sombra da falta de emoção, da insensibilidade e da indiferença.',
        'personalidade': 'A cor cinza azulado pode indicar uma personalidade harmoniosa, tranquila e serena.',
        'diagnostico': 'O uso excessivo da cor cinza azulado pode indicar uma tendência à falta de emoção, insensibilidade ou indiferença.'
    },
    '35': {
        'cor': 'Rosa antigo',
        'rgb': (188, 143, 143),
        'anima_animus': 'O rosa antigo representa a nostalgia, a delicadeza e a suavidade.',
        'sombra': 'O rosa antigo é a sombra da melancolia, da sensibilidade excessiva e da falta de assertividade.',
        'personalidade': 'A cor rosa antigo pode indicar uma personalidade nostálgica, delicada e suave.',
        'diagnostico': 'O uso excessivo da cor rosa antigo pode indicar uma tendência à melancolia, sensibilidade excessiva ou falta de assertividade.'
    },
    '36': {
        'cor': 'Roxo escuro',
        'rgb': (72, 61, 139),
        'anima_animus': 'O roxo escuro representa a espiritualidade profunda, a intuição e o mistério.',
        'sombra': 'O roxo escuro é a sombra do fanatismo, da manipulação emocional e da falta de conexão com a realidade.',
        'personalidade': 'A cor roxa escuro pode indicar uma personalidade com espiritualidade profunda, intuitiva e misteriosa.',
        'diagnostico': 'O uso excessivo da cor roxa escuro pode indicar uma tendência ao fanatismo, manipulação emocional ou falta de conexão com a realidade.'
    },
    '37': {
        'cor': 'Ouro rosa',
        'rgb': (215, 170, 135),
        'anima_animus': 'O ouro rosa representa a elegância, a delicadeza e a sutileza.',
        'sombra': 'O ouro rosa é a sombra da superficialidade, da falta de profundidade emocional e da falta de autenticidade.',
        'personalidade': 'A cor ouro rosa pode indicar uma personalidade elegante, delicada e sutil.',
        'diagnostico': 'O uso excessivo da cor ouro rosa pode indicar uma tendência à superficialidade, falta de profundidade emocional ou falta de autenticidade.'
    },
    '38': {
        'cor': 'Coral',
        'rgb': (255, 127, 80),
        'anima_animus': 'O coral representa a paixão, a criatividade e a expressão emocional.',
        'sombra': 'O coral é a sombra da intensidade emocional, da impulsividade e do drama.',
        'personalidade': 'A cor coral pode indicar uma personalidade apaixonada, criativa e expressiva emocionalmente.',
        'diagnostico': 'O uso excessivo da cor coral pode indicar uma tendência à intensidade emocional, impulsividade ou drama.'
    },
    '39': {
        'cor': 'Verde menta',
        'rgb': (152, 251, 152),
        'anima_animus': 'O verde menta representa o equilíbrio emocional, a renovação e a harmonia.',
        'sombra': 'O verde menta é a sombra da instabilidade emocional, da indecisão e do conflito interno.',
        'personalidade': 'A cor verde menta pode indicar uma personalidade com equilíbrio emocional, renovação e harmonia.',
        'diagnostico': 'O uso excessivo da cor verde menta pode indicar uma tendência à instabilidade emocional, indecisão ou conflito interno.'
    },
    '40': {
        'cor': 'Laranja claro',
        'rgb': (255, 204, 153),
        'anima_animus': 'O laranja claro representa a alegria, a criatividade e a sociabilidade.',
        'sombra': 'O laranja claro é a sombra da falta de foco, da dispersão e da superficialidade nas relações.',
        'personalidade': 'A cor laranja claro pode indicar uma personalidade alegre, criativa e sociável.',
        'diagnostico': 'O uso excessivo da cor laranja claro pode indicar uma tendência à falta de foco, dispersão ou superficialidade nas relações.'
    },
    '41': {
        'cor': 'Rosa vibrante',
        'rgb': (255, 0, 127),
        'anima_animus': 'O rosa vibrante representa a paixão intensa, a sensualidade e a autoexpressão.',
        'sombra': 'O rosa vibrante é a sombra da dependência emocional, da manipulação e do drama excessivo.',
        'personalidade': 'A cor rosa vibrante pode indicar uma personalidade com paixão intensa, sensualidade e autoexpressão.',
        'diagnostico': 'O uso excessivo da cor rosa vibrante pode indicar uma tendência à dependência emocional, manipulação ou drama excessivo.'
    },
    '42': {
        'cor': 'Verde esmeralda',
        'rgb': (0, 201, 87),
        'anima_animus': 'O verde esmeralda representa a prosperidade, a cura e a renovação.',
        'sombra': 'O verde esmeralda é a sombra da inveja, da ganância e da falta de gratidão.',
        'personalidade': 'A cor verde esmeralda pode indicar uma personalidade próspera, curativa e em constante renovação.',
        'diagnostico': 'O uso excessivo da cor verde esmeralda pode indicar uma tendência à inveja, ganância ou falta de gratidão.'
    },
    '43': {
        'cor': 'Azul royal',
        'rgb': (65, 105, 225),
        'anima_animus': 'O azul royal representa a confiança, a liderança e a autoridade.',
        'sombra': 'O azul royal é a sombra do autoritarismo, da rigidez e da falta de empatia.',
        'personalidade': 'A cor azul royal pode indicar uma personalidade confiante, líder e com autoridade.',
        'diagnostico': 'O uso excessivo da cor azul royal pode indicar uma tendência ao autoritarismo, rigidez ou falta de empatia.'
    },
    '44': {
        'cor': 'Cinza azulado claro',
        'rgb': (176, 224, 230),
        'anima_animus': 'O cinza azulado claro representa a tranquilidade, a paz e a serenidade interior.',
        'sombra': 'O cinza azulado claro é a sombra da falta de emoção, da insensibilidade e da indiferença emocional.',
        'personalidade': 'A cor cinza azulado claro pode indicar uma personalidade tranquila, pacífica e serena interiormente.',
        'diagnostico': 'O uso excessivo da cor cinza azulado claro pode indicar uma tendência à falta de emoção, insensibilidade ou indiferença emocional.'
    },
    '45': {
        'cor': 'Lilás claro',
        'rgb': (229, 204, 255),
        'anima_animus': 'O lilás claro representa a espiritualidade sutil, a intuição e a sensibilidade.',
        'sombra': 'O lilás claro é a sombra da falta de discernimento espiritual, da ingenuidade e da vulnerabilidade emocional.',
        'personalidade': 'A cor lilás claro pode indicar uma personalidade com espiritualidade sutil, intuição e sensibilidade.',
        'diagnostico': 'O uso excessivo da cor lilás claro pode indicar uma tendência à falta de discernimento espiritual, ingenuidade ou vulnerabilidade emocional.'
    },
    '46': {
        'cor': 'Bege claro',
        'rgb': (255, 255, 224),
        'anima_animus': 'O bege claro representa a simplicidade, a calma e a estabilidade emocional.',
        'sombra': 'O bege claro é a sombra da falta de individualidade, da falta de ambição e da falta de paixão.',
        'personalidade': 'A cor bege claro pode indicar uma personalidade simples, calma e emocionalmente estável.',
        'diagnostico': 'O uso excessivo da cor bege claro pode indicar uma tendência à falta de individualidade, falta de ambição ou falta de paixão.'
    },
    '47': {
        'cor': 'Azul meia-noite',
        'rgb': (25, 25, 112),
        'anima_animus': 'O azul meia-noite representa a profundidade emocional, a introspecção e a sabedoria interior.',
        'sombra': 'O azul meia-noite é a sombra da depressão, da falta de clareza emocional e do isolamento.',
        'personalidade': 'A cor azul meia-noite pode indicar uma personalidade com profundidade emocional, introspecção e sabedoria interior.',
        'diagnostico': 'O uso excessivo da cor azul meia-noite pode indicar uma tendência à depressão, falta de clareza emocional ou isolamento.'
    },
    '48': {
        'cor': 'Verde pistache',
        'rgb': (185, 218, 144),
        'anima_animus': 'O verde pistache representa o equilíbrio emocional, a renovação e a harmonia.',
        'sombra': 'O verde pistache é a sombra da indecisão, da falta de comprometimento e do conflito interno.',
        'personalidade': 'A cor verde pistache pode indicar uma personalidade com equilíbrio emocional, renovação e harmonia.',
        'diagnostico': 'O uso excessivo da cor verde pistache pode indicar uma tendência à indecisão, falta de comprometimento ou conflito interno.'
    },
    '49': {
        'cor': 'Coral claro',
        'rgb': (240, 128, 128),
        'anima_animus': 'O coral claro representa a alegria suave, a delicadeza e a expressão emocional sutil.',
        'sombra': 'O coral claro é a sombra da dependência emocional sutil, da manipulação sutil e da falta de clareza emocional.',
        'personalidade': 'A cor coral claro pode indicar uma personalidade com alegria suave, delicadeza e expressão emocional sutil.',
        'diagnostico': 'O uso excessivo da cor coral claro pode indicar uma tendência à dependência emocional sutil, manipulação sutil ou falta de clareza emocional.'
    },
    '50': {
        'cor': 'Verde oliva claro',
        'rgb': (188, 208, 124),
        'anima_animus': 'O verde oliva claro representa a estabilidade emocional, a segurança e a conexão com a natureza.',
        'sombra': 'O verde oliva claro é a sombra da rigidez emocional, da falta de adaptabilidade e da falta de equilíbrio interior.',
        'personalidade': 'A cor verde oliva claro pode indicar uma personalidade com estabilidade emocional, segurança e conexão com a natureza.',
        'diagnostico': 'O uso excessivo da cor verde oliva claro pode indicar uma tendência à rigidez emocional, falta de adaptabilidade ou falta de equilíbrio interior.'
    }
}

# Adicionando à lista sem repetir a numeração do RGB
lista_cores.extend([cor for cor in cores.values() if cor['rgb'] not in [c['rgb'] for c in lista_cores]])

print("Lista atualizada de cores:")
for cor in lista_cores:
    print(f"Cor: {cor['cor']} | RGB: {cor['rgb']}")
