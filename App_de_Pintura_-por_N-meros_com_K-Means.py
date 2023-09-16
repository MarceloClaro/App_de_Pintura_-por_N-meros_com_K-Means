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
        'cor': 'Branco',
        'rgb': (255, 255, 255),
        'anima_animus': 'A cor branca representa a busca pela integridade e totalidade, simbolizando a pureza e a clareza da mente.',
        'sombra': 'A cor branca pode representar a negação da sombra e a repressão de aspectos obscuros da personalidade.',
        'personalidade': 'A cor branca pode ser associada a uma personalidade pura, inocente e espiritual.',
        'diagnostico': 'Em excesso, a cor branca pode indicar uma fuga da realidade ou da confrontação com aspectos sombrios.'
    },
    '3': {
        'cor': 'Vermelho',
        'rgb': (255, 0, 0),
        'anima_animus': 'O vermelho representa a paixão, a energia e o desejo. É a cor do impulso e da força vital.',
        'sombra': 'O vermelho pode representar agressão, raiva e impulsividade quando não controlado.',
        'personalidade': 'Pessoas que preferem o vermelho podem ser apaixonadas, corajosas e enérgicas.',
        'diagnostico': 'Em excesso, o vermelho pode indicar hostilidade ou comportamento agressivo.'
    },
    '4': {
        'cor': 'Azul',
        'rgb': (0, 0, 255),
        'anima_animus': 'O azul representa a busca pelo significado e a espiritualidade. É a cor da serenidade e da profundidade emocional.',
        'sombra': 'Em sua sombra, o azul pode representar frieza emocional e distanciamento.',
        'personalidade': 'Pessoas que se identificam com o azul podem ser tranquilas, espirituais e comunicativas.',
        'diagnostico': 'Em excesso, o azul pode indicar repressão emocional e isolamento.'
    },
    '5': {
        'cor': 'Amarelo',
        'rgb': (255, 255, 0),
        'anima_animus': 'O amarelo simboliza a luz, a iluminação e a busca pelo autoconhecimento. É a cor da alegria e do otimismo.',
        'sombra': 'O amarelo pode representar superficialidade, egocentrismo e falta de profundidade emocional.',
        'personalidade': 'Pessoas que preferem o amarelo podem ser otimistas, intelectuais e criativas.',
        'diagnostico': 'Em excesso, o amarelo pode indicar superficialidade ou falta de autenticidade.'
    },
    '6': {
        'cor': 'Verde',
        'rgb': (0, 255, 0),
        'anima_animus': 'O verde simboliza o equilíbrio, a harmonia e a cura. É a cor da natureza e do crescimento.',
        'sombra': 'O verde pode representar inveja, ciúmes e rivalidade.',
        'personalidade': 'Pessoas que preferem o verde podem ser compassivas, equilibradas e voltadas para a cura.',
        'diagnostico': 'Em excesso, o verde pode indicar uma obsessão com a harmonia ou a inveja.'
    },
    '7': {
        'cor': 'Roxo',
        'rgb': (128, 0, 128),
        'anima_animus': 'O roxo representa a espiritualidade, a intuição e a transcendência. É a cor da sabedoria e da conexão espiritual.',
        'sombra': 'O roxo pode representar uma desconexão com a realidade ou a busca por experiências espirituais extremas.',
        'personalidade': 'Pessoas que preferem o roxo podem ser intuitivas, espirituais e criativas.',
        'diagnostico': 'Em excesso, o roxo pode indicar uma fuga da realidade ou uma busca obsessiva pela espiritualidade.'
    },
    '8': {
        'cor': 'Laranja',
        'rgb': (255, 165, 0),
        'anima_animus': 'O laranja representa a energia criativa e a expressão. É a cor da alegria de viver e da sociabilidade.',
        'sombra': 'Em sua sombra, o laranja pode representar impulsividade e excesso de energia.',
        'personalidade': 'Pessoas que preferem o laranja podem ser extrovertidas, sociais e entusiastas.',
        'diagnostico': 'Em excesso, o laranja pode indicar hiperatividade ou falta de controle.'
    },
    '9': {
        'cor': 'Cinza',
        'rgb': (128, 128, 128),
        'anima_animus': 'O cinza representa a neutralidade e a indiferença. É a cor da ausência de emoções fortes.',
        'sombra': 'O cinza pode representar apatia e falta de envolvimento emocional.',
        'personalidade': 'Pessoas que preferem o cinza podem ser objetivas, práticas e equilibradas emocionalmente.',
        'diagnostico': 'Em excesso, o cinza pode indicar uma falta de paixão ou uma sensação de vazio.'
    },
    '10': {
        'cor': 'Marrom',
        'rgb': (139, 69, 19),
        'anima_animus': 'O marrom representa a terra, a estabilidade e a segurança. É a cor da conexão com a natureza.',
        'sombra': 'O marrom pode representar teimosia e resistência a mudanças.',
        'personalidade': 'Pessoas que preferem o marrom podem ser práticas, realistas e ligadas à terra.',
        'diagnostico': 'Em excesso, o marrom pode indicar rigidez ou relutância em se adaptar.'
    },
    '11': {
        'cor': 'Rosa',
        'rgb': (255, 192, 203),
        'anima_animus': 'O rosa representa o amor, a compaixão e a ternura. É a cor do afeto e do cuidado.',
        'sombra': 'O rosa pode representar ingenuidade e falta de maturidade emocional.',
        'personalidade': 'Pessoas que preferem o rosa podem ser amorosas, carinhosas e sensíveis.',
        'diagnostico': 'Em excesso, o rosa pode indicar uma dependência excessiva de outros ou uma falta de firmeza.'
    },
    '12': {
        'cor': 'Dourado',
        'rgb': (255, 215, 0),
        'anima_animus': 'O dourado representa a riqueza, o sucesso e a autoestima elevada. É a cor da realização pessoal.',
        'sombra': 'O dourado pode representar arrogância e busca excessiva por status.',
        'personalidade': 'Pessoas que preferem o dourado podem ser confiantes, ambiciosas e autoconfiantes.',
        'diagnostico': 'Em excesso, o dourado pode indicar uma obsessão por riqueza ou poder.'
    },
    '13': {
        'cor': 'Prateado',
        'rgb': (192, 192, 192),
        'anima_animus': 'O prateado representa a intuição e a sensibilidade psíquica. É a cor da conexão com o inconsciente.',
        'sombra': 'O prateado pode representar confusão mental e evasão da realidade.',
        'personalidade': 'Pessoas que preferem o prateado podem ser espiritualmente sensíveis, intuitivas e introspectivas.',
        'diagnostico': 'Em excesso, o prateado pode indicar uma desconexão com a realidade.'
    },
    '14': {
        'cor': 'Turquesa',
        'rgb': (64, 224, 208),
        'anima_animus': 'O turquesa representa a comunicação e a expressão criativa. É a cor da clareza mental e da inovação.',
        'sombra': 'O turquesa pode representar superficialidade e falta de foco.',
        'personalidade': 'Pessoas que preferem o turquesa podem ser comunicativas, criativas e adaptáveis.',
        'diagnostico': 'Em excesso, o turquesa pode indicar uma falta de profundidade emocional.'
    },
    '15': {
        'cor': 'Ouro',
        'rgb': (255, 215, 0),
        'anima_animus': 'O ouro representa a riqueza, o sucesso e a autoestima elevada. É a cor da realização pessoal.',
        'sombra': 'O ouro pode representar arrogância e busca excessiva por status.',
        'personalidade': 'Pessoas que preferem o ouro podem ser confiantes, ambiciosas e autoconfiantes.',
        'diagnostico': 'Em excesso, o ouro pode indicar uma obsessão por riqueza ou poder.'
    },
    '16': {
        'cor': 'Azul Claro',
        'rgb': (173, 216, 230),
        'anima_animus': 'O azul claro representa a calma, a clareza e a abertura para novas ideias. É a cor da mente tranquila.',
        'sombra': 'O azul claro pode representar falta de firmeza e indecisão.',
        'personalidade': 'Pessoas que preferem o azul claro podem ser pacíficas, equilibradas e abertas a novas perspectivas.',
        'diagnostico': 'Em excesso, o azul claro pode indicar falta de assertividade ou conformismo.'
    },
    '17': {
        'cor': 'Verde Claro',
        'rgb': (144, 238, 144),
        'anima_animus': 'O verde claro representa a renovação, o crescimento e a cura. É a cor da esperança e da vitalidade.',
        'sombra': 'O verde claro pode representar inconstância e falta de comprometimento.',
        'personalidade': 'Pessoas que preferem o verde claro podem ser otimistas, rejuvenescedoras e comprometidas com o crescimento pessoal.',
        'diagnostico': 'Em excesso, o verde claro pode indicar falta de foco ou superficialidade.'
    },
    '18': {
        'cor': 'Violeta',
        'rgb': (238, 130, 238),
        'anima_animus': 'O violeta representa a espiritualidade elevada e a transformação. É a cor da busca por significado profundo.',
        'sombra': 'O violeta pode representar uma busca obsessiva por significado e desconexão com o mundo material.',
        'personalidade': 'Pessoas que preferem o violeta podem ser profundas, espirituais e transformadoras.',
        'diagnostico': 'Em excesso, o violeta pode indicar uma desconexão com a realidade terrena.'
    },
    '19': {
        'cor': 'Prata',
        'rgb': (192, 192, 192),
        'anima_animus': 'O prateado representa a intuição e a sensibilidade psíquica. É a cor da conexão com o inconsciente.',
        'sombra': 'O prateado pode representar confusão mental e evasão da realidade.',
        'personalidade': 'Pessoas que preferem o prateado podem ser espiritualmente sensíveis, intuitivas e introspectivas.',
        'diagnostico': 'Em excesso, o prateado pode indicar uma desconexão com a realidade.'
    },
    '20': {
        'cor': 'Ciano',
        'rgb': (0, 255, 255),
        'anima_animus': 'O ciano representa a comunicação clara e a lógica. É a cor da mente analítica e da expressão precisa.',
        'sombra': 'O ciano pode representar rigidez mental e falta de empatia.',
        'personalidade': 'Pessoas que preferem o ciano podem ser lógicas, comunicativas e objetivas.',
        'diagnostico': 'Em excesso, o ciano pode indicar falta de sensibilidade emocional ou excesso de crítica.'
    },
    '21': {
        'cor': 'Lilás',
        'rgb': (128, 0, 128),
        'anima_animus': 'O lilás representa a espiritualidade elevada e a busca por respostas profundas. É a cor da transformação interior.',
        'sombra': 'O lilás pode representar uma busca obsessiva por respostas espirituais e desconexão com a realidade cotidiana.',
        'personalidade': 'Pessoas que preferem o lilás podem ser espiritualmente conscientes, buscadoras e transformadoras.',
        'diagnostico': 'Em excesso, o lilás pode indicar uma fuga da realidade terrena.'
    },
    '22': {
        'cor': 'Rosa Claro',
        'rgb': (255, 182, 193),
        'anima_animus': 'O rosa claro representa a doçura, a delicadeza e a empatia. É a cor da compreensão e do cuidado com os outros.',
        'sombra': 'O rosa claro pode representar fragilidade emocional e dependência excessiva dos outros.',
        'personalidade': 'Pessoas que preferem o rosa claro podem ser carinhosas, gentis e compassivas.',
        'diagnostico': 'Em excesso, o rosa claro pode indicar uma falta de independência emocional.'
    },
    '23': {
        'cor': 'Dourado Claro',
        'rgb': (255, 223, 186),
        'anima_animus': 'O dourado claro representa a espiritualidade elevada e a busca pela iluminação. É a cor da conexão com o divino.',
        'sombra': 'O dourado claro pode representar uma busca obsessiva por iluminação espiritual e desconexão com a vida terrena.',
        'personalidade': 'Pessoas que preferem o dourado claro podem ser espiritualmente iluminadas, buscadoras e conectadas com o divino.',
        'diagnostico': 'Em excesso, o dourado claro pode indicar uma fuga da realidade material.'
    },
    '24': {
        'cor': 'Cinza Claro',
        'rgb': (211, 211, 211),
        'anima_animus': 'O cinza claro representa a neutralidade e a objetividade. É a cor da mente equilibrada e imparcial.',
        'sombra': 'O cinza claro pode representar falta de personalidade e indecisão.',
        'personalidade': 'Pessoas que preferem o cinza claro podem ser imparciais, objetivas e equilibradas emocionalmente.',
        'diagnostico': 'Em excesso, o cinza claro pode indicar falta de identidade própria.'
    },
    '25': {
        'cor': 'Azul Escuro',
        'rgb': (0, 0, 139),
        'anima_animus': 'O azul escuro representa a profundidade emocional e a busca por significado. É a cor da introspecção e da reflexão.',
        'sombra': 'O azul escuro pode representar depressão e isolamento emocional.',
        'personalidade': 'Pessoas que preferem o azul escuro podem ser introspectivas, pensativas e voltadas para o significado da vida.',
        'diagnostico': 'Em excesso, o azul escuro pode indicar um isolamento excessivo.'
    },
    '26': {
        'cor': 'Amarelo Claro',
        'rgb': (255, 255, 224),
        'anima_animus': 'O amarelo claro representa a alegria e a positividade. É a cor da energia e do entusiasmo.',
        'sombra': 'O amarelo claro pode representar superficialidade e excesso de otimismo.',
        'personalidade': 'Pessoas que preferem o amarelo claro podem ser alegres, entusiastas e cheias de energia.',
        'diagnostico': 'Em excesso, o amarelo claro pode indicar uma falta de realismo.'
    },
    '27': {
        'cor': 'Verde Escuro',
        'rgb': (0, 100, 0),
        'anima_animus': 'O verde escuro representa a ligação com a natureza e a estabilidade emocional. É a cor da tranquilidade e da segurança.',
        'sombra': 'O verde escuro pode representar teimosia e resistência a mudanças.',
        'personalidade': 'Pessoas que preferem o verde escuro podem ser estáveis, ligadas à terra e protetoras.',
        'diagnostico': 'Em excesso, o verde escuro pode indicar rigidez emocional.'
    },
    '28': {
        'cor': 'Bege',
        'rgb': (245, 245, 220),
        'anima_animus': 'O bege representa a simplicidade e a neutralidade. É a cor da calma e da discrição.',
        'sombra': 'O bege pode representar falta de expressão e falta de individualidade.',
        'personalidade': 'Pessoas que preferem o bege podem ser simples, discretas e pacíficas.',
        'diagnostico': 'Em excesso, o bege pode indicar falta de originalidade.'
    },
    '29': {
        'cor': 'Roxo Escuro',
        'rgb': (148, 0, 211),
        'anima_animus': 'O roxo escuro representa a espiritualidade profunda e a transformação interior. É a cor da busca por significado.',
        'sombra': 'O roxo escuro pode representar uma busca obsessiva por significado e desconexão com o mundo material.',
        'personalidade': 'Pessoas que preferem o roxo escuro podem ser espiritualmente conscientes, transformadoras e profundas.',
        'diagnostico': 'Em excesso, o roxo escuro pode indicar uma fuga da realidade terrena.'
    },
    '30': {
        'cor': 'Pêssego',
        'rgb': (255, 229, 180),
        'anima_animus': 'O pêssego representa a doçura e a empatia. É a cor da compreensão e da gentileza.',
        'sombra': 'O pêssego pode representar falta de firmeza e dependência excessiva dos outros.',
        'personalidade': 'Pessoas que preferem o pêssego podem ser carinhosas, sensíveis e compassivas.',
        'diagnostico': 'Em excesso, o pêssego pode indicar uma falta de independência emocional.'
    },
    '31': {
        'cor': 'Bronze',
        'rgb': (205, 127, 50),
        'anima_animus': 'O bronze representa a conquista e o reconhecimento. É a cor da realização pessoal e da autoestima elevada.',
        'sombra': 'O bronze pode representar arrogância e busca excessiva por reconhecimento.',
        'personalidade': 'Pessoas que preferem o bronze podem ser confiantes, ambiciosas e autoconfiantes.',
        'diagnostico': 'Em excesso, o bronze pode indicar uma obsessão por reconhecimento social.'
    },
    '32': {
        'cor': 'Vinho',
        'rgb': (128, 0, 0),
        'anima_animus': 'O vinho representa a sensualidade e a paixão. É a cor do desejo e da intensidade emocional.',
        'sombra': 'O vinho pode representar impulsividade e comportamento autodestrutivo quando não controlado.',
        'personalidade': 'Pessoas que preferem o vinho podem ser sensuais, intensas e emocionais.',
        'diagnostico': 'Em excesso, o vinho pode indicar uma tendência a comportamentos autodestrutivos.'
    },
    '33': {
        'cor': 'Dourado Escuro',
        'rgb': (184, 134, 11),
        'anima_animus': 'O dourado escuro representa a busca por riqueza e poder. É a cor da ambição e da ostentação.',
        'sombra': 'O dourado escuro pode representar ganância e busca excessiva por status.',
        'personalidade': 'Pessoas que preferem o dourado escuro podem ser ambiciosas, materialistas e ostentadoras.',
        'diagnostico': 'Em excesso, o dourado escuro pode indicar uma obsessão por riqueza e poder.'
    },
    '34': {
        'cor': 'Marrom Claro',
        'rgb': (222, 184, 135),
        'anima_animus': 'O marrom claro representa a conexão com a terra e a estabilidade emocional. É a cor da segurança e do acolhimento.',
        'sombra': 'O marrom claro pode representar teimosia e resistência a mudanças.',
        'personalidade': 'Pessoas que preferem o marrom claro podem ser estáveis, acolhedoras e ligadas à terra.',
        'diagnostico': 'Em excesso, o marrom claro pode indicar rigidez emocional.'
    },
    '35': {
        'cor': 'Pêssego Claro',
        'rgb': (255, 218, 185),
        'anima_animus': 'O pêssego claro representa a doçura e a empatia. É a cor da compreensão e da gentileza.',
        'sombra': 'O pêssego claro pode representar falta de firmeza e dependência excessiva dos outros.',
        'personalidade': 'Pessoas que preferem o pêssego claro podem ser carinhosas, sensíveis e compassivas.',
        'diagnostico': 'Em excesso, o pêssego claro pode indicar uma falta de independência emocional.'
    },
    '36': {
        'cor': 'Bronze Claro',
        'rgb': (205, 155, 29),
        'anima_animus': 'O bronze claro representa a busca por conquistas e reconhecimento. É a cor da autoestima elevada e da realização pessoal.',
        'sombra': 'O bronze claro pode representar busca excessiva por reconhecimento e narcisismo.',
        'personalidade': 'Pessoas que preferem o bronze claro podem ser confiantes, ambiciosas e autoconfiantes.',
        'diagnostico': 'Em excesso, o bronze claro pode indicar uma obsessão por reconhecimento social.'
    },
    '37': {
        'cor': 'Lavanda',
        'rgb': (230, 230, 250),
        'anima_animus': 'A lavanda representa a espiritualidade elevada e a busca por paz interior. É a cor da tranquilidade e da compaixão.',
        'sombra': 'A lavanda pode representar uma busca obsessiva por paz interior e desconexão com a realidade.',
        'personalidade': 'Pessoas que preferem a lavanda podem ser espiritualmente conscientes, pacíficas e compreensivas.',
        'diagnostico': 'Em excesso, a lavanda pode indicar uma fuga da realidade terrena.'
    },
    '38': {
        'cor': 'Salmon',
        'rgb': (250, 128, 114),
        'anima_animus': 'O salmon representa a emoção e a expressão autêntica. É a cor da intensidade emocional e da empatia.',
        'sombra': 'O salmon pode representar emocionalismo excessivo e falta de controle emocional.',
        'personalidade': 'Pessoas que preferem o salmon podem ser emocionais, expressivas e empáticas.',
        'diagnostico': 'Em excesso, o salmon pode indicar dificuldade em controlar as emoções.'
    },
    '39': {
        'cor': 'Ocre',
        'rgb': (204, 119, 34),
        'anima_animus': 'O ocre representa a conexão com a terra e a estabilidade emocional. É a cor da segurança e do enraizamento.',
        'sombra': 'O ocre pode representar teimosia e resistência a mudanças.',
        'personalidade': 'Pessoas que preferem o ocre podem ser estáveis, enraizadas e protetoras.',
        'diagnostico': 'Em excesso, o ocre pode indicar rigidez emocional.'
    },
    '40': {
        'cor': 'Coral',
        'rgb': (255, 127, 80),
        'anima_animus': 'O coral representa a emoção e a expressão autêntica. É a cor da intensidade emocional e da paixão.',
        'sombra': 'O coral pode representar impulsividade e reatividade emocional.',
        'personalidade': 'Pessoas que preferem o coral podem ser apaixonadas, expressivas e intensas.',
        'diagnostico': 'Em excesso, o coral pode indicar dificuldade em controlar as emoções.'
    },
    '41': {
        'cor': 'Bege Claro',
        'rgb': (245, 245, 220),
        'anima_animus': 'O bege claro representa a simplicidade e a neutralidade. É a cor da calma e da discrição.',
        'sombra': 'O bege claro pode representar falta de expressão e falta de individualidade.',
        'personalidade': 'Pessoas que preferem o bege claro podem ser simples, discretas e pacíficas.',
        'diagnostico': 'Em excesso, o bege claro pode indicar falta de originalidade.'
    },
    '42': {
        'cor': 'Oliveira',
        'rgb': (128, 128, 0),
        'anima_animus': 'O oliveira representa a estabilidade e a conexão com a natureza. É a cor da harmonia e da prosperidade.',
        'sombra': 'O oliveira pode representar teimosia e resistência a mudanças.',
        'personalidade': 'Pessoas que preferem o oliveira podem ser equilibradas, ligadas à natureza e prósperas.',
        'diagnostico': 'Em excesso, o oliveira pode indicar uma rigidez emocional.'
    },
    '43': {
        'cor': 'Rosa Escuro',
        'rgb': (255, 20, 147),
        'anima_animus': 'O rosa escuro representa a sensualidade e a paixão. É a cor da intensidade emocional e da conexão íntima.',
        'sombra': 'O rosa escuro pode representar dependência emocional excessiva e comportamentos autodestrutivos.',
        'personalidade': 'Pessoas que preferem o rosa escuro podem ser sensuais, intensas e emocionais.',
        'diagnostico': 'Em excesso, o rosa escuro pode indicar uma tendência a comportamentos autodestrutivos.'
    },
    '44': {
        'cor': 'Cobre',
        'rgb': (184, 115, 51),
        'anima_animus': 'O cobre representa a busca por conquistas e sucesso material. É a cor da ambição e da realização pessoal.',
        'sombra': 'O cobre pode representar ganância e busca excessiva por status.',
        'personalidade': 'Pessoas que preferem o cobre podem ser confiantes, ambiciosas e voltadas para o sucesso.',
        'diagnostico': 'Em excesso, o cobre pode indicar uma obsessão por sucesso material.'
    },
    '45': {
        'cor': 'Amarelo Escuro',
        'rgb': (255, 204, 0),
        'anima_animus': 'O amarelo escuro representa a criatividade e a expressão. É a cor da originalidade e do entusiasmo criativo.',
        'sombra': 'O amarelo escuro pode representar egocentrismo e busca excessiva por reconhecimento.',
        'personalidade': 'Pessoas que preferem o amarelo escuro podem ser criativas, entusiastas e autoexpressivas.',
        'diagnostico': 'Em excesso, o amarelo escuro pode indicar uma busca obsessiva por reconhecimento.'
    },
    '46': {
        'cor': 'Laranja Escuro',
        'rgb': (255, 140, 0),
        'anima_animus': 'O laranja escuro representa a energia e a ação. É a cor da iniciativa e da coragem.',
        'sombra': 'O laranja escuro pode representar impulsividade e falta de controle.',
        'personalidade': 'Pessoas que preferem o laranja escuro podem ser enérgicas, corajosas e empreendedoras.',
        'diagnostico': 'Em excesso, o laranja escuro pode indicar hiperatividade ou falta de controle.'
    },
    '47': {
        'cor': 'Cinza Escuro',
        'rgb': (64, 64, 64),
        'anima_animus': 'O cinza escuro representa a neutralidade e a introspecção. É a cor da reflexão profunda e da análise.',
        'sombra': 'O cinza escuro pode representar isolamento emocional e falta de expressão.',
        'personalidade': 'Pessoas que preferem o cinza escuro podem ser analíticas, introspectivas e reservadas.',
        'diagnostico': 'Em excesso, o cinza escuro pode indicar uma desconexão com as emoções.'
    },
    '48': {
        'cor': 'Verde Musgo',
        'rgb': (128, 128, 0),
        'anima_animus': 'O verde musgo representa a conexão com a natureza e a estabilidade emocional. É a cor da harmonia e do enraizamento.',
        'sombra': 'O verde musgo pode representar teimosia e resistência a mudanças.',
        'personalidade': 'Pessoas que preferem o verde musgo podem ser equilibradas, ligadas à natureza e estáveis emocionalmente.',
        'diagnostico': 'Em excesso, o verde musgo pode indicar rigidez emocional.'
    },
    '49': {
        'cor': 'Turquesa Escuro',
        'rgb': (0, 206, 209),
        'anima_animus': 'O turquesa escuro representa a comunicação clara e a criatividade. É a cor da expressão precisa e da inovação.',
        'sombra': 'O turquesa escuro pode representar rigidez mental e falta de empatia.',
        'personalidade': 'Pessoas que preferem o turquesa escuro podem ser comunicativas, criativas e objetivas.',
        'diagnostico': 'Em excesso, o turquesa escuro pode indicar falta de sensibilidade emocional ou excesso de crítica.'
    },
    '50': {
        'cor': 'Ouro Escuro',
        'rgb': (184, 134, 11),
        'anima_animus': 'O ouro escuro representa a busca por riqueza e poder. É a cor da ambição e da ostentação.',
        'sombra': 'O ouro escuro pode representar ganância e busca excessiva por status.',
        'personalidade': 'Pessoas que preferem o ouro escuro podem ser ambiciosas, materialistas e ostentadoras.',
        'diagnostico': 'Em excesso, o ouro escuro pode indicar uma obsessão por riqueza e poder.'
    }
}

# Lembre-se de que a interpretação das cores e suas associações com traços de personalidade podem variar de pessoa para pessoa e não devem ser consideradas definitivas. A psicologia das cores é um campo de estudo complexo e subjetivo.


# Aqui estamos criando uma nova ferramenta que chamamos de "Canvas".
# Isso nos ajuda a lidar com imagens e cores.

def rgb_to_cmyk(r, g, b):
    if (r == 0) and (g == 0) and (b == 0):
        return 0, 0, 0, 1
    c = 1 - r / 255
    m = 1 - g / 255
    y = 1 - b / 255

    min_cmy = min(c, m, y)
    c = (c - min_cmy) / (1 - min_cmy)
    m = (m - min_cmy) / (1 - min_cmy)
    y = (y - min_cmy) / (1 - min_cmy)
    k = min_cmy

    return c, m, y, k

def calculate_ml(c, m, y, k, total_ml):
    total_ink = c + m + y + k
    c_ml = (c / total_ink) * total_ml
    m_ml = (m / total_ink) * total_ml
    y_ml = (y / total_ink) * total_ml
    k_ml = (k / total_ink) * total_ml
    return c_ml, m_ml, y_ml, k_ml

def buscar_cor_proxima(rgb, cores_junguianas):
    distancias = []
    for cor_junguiana in cores_junguianas.values():
        cor_junguiana_rgb = cor_junguiana['rgb']
        distancia = np.sqrt(np.sum((np.array(rgb) - np.array(cor_junguiana_rgb)) ** 2))
        distancias.append(distancia)
    cor_proxima_index = np.argmin(distancias)
    return cores_junguianas[str(cor_proxima_index + 1)]

class Canvas():
    def __init__(self, src, nb_color, pixel_size=4000):
        self.src = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)  # Corrige a ordem dos canais de cor
        self.nb_color = nb_color
        self.tar_width = pixel_size
        self.colormap = []

    def generate(self):
        im_source = self.resize()
        clean_img = self.cleaning(im_source)
        width, height, depth = clean_img.shape
        clean_img = np.array(clean_img, dtype="uint8") / 255
        quantified_image, colors = self.quantification(clean_img)
        canvas = np.ones(quantified_image.shape[:2], dtype="uint8") * 255

        for ind, color in enumerate(colors):
            self.colormap.append([int(c * 255) for c in color])
            mask = cv2.inRange(quantified_image, color, color)
            cnts = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
            cnts = cnts[0] if len(cnts) == 2 else cnts[1]

            for contour in cnts:
                _, _, width_ctr, height_ctr = cv2.boundingRect(contour)
                if width_ctr > 10 and height_ctr > 10 and cv2.contourArea(contour, True) < -100:
                    cv2.drawContours(canvas, [contour], -1, (0, 0, 0), 1)
                    txt_x, txt_y = contour[0][0]
                    cv2.putText(canvas, '{:d}'.format(ind + 1), (txt_x, txt_y + 15),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

        return canvas, colors, quantified_image

    def resize(self):
        (height, width) = self.src.shape[:2]
        if height > width:  # modo retrato
            dim = (int(width * self.tar_width / float(height)), self.tar_width)
        else:
            dim = (self.tar_width, int(height * self.tar_width / float(width)))
        return cv2.resize(self.src, dim, interpolation=cv2.INTER_AREA)

    def cleaning(self, picture):
        clean_pic = cv2.fastNlMeansDenoisingColored(picture, None, 10, 10, 7, 21)
        kernel = np.ones((5, 5), np.uint8)
        img_erosion = cv2.erode(clean_pic, kernel, iterations=1)
        img_dilation = cv2.dilate(img_erosion, kernel, iterations=1)
        return img_dilation

    def quantification(self, picture):
        width, height, depth = picture.shape
        flattened = np.reshape(picture, (width * height, depth))
        sample = shuffle(flattened)[:1000]
        kmeans = KMeans(n_clusters=self.nb_color).fit(sample)
        labels = kmeans.predict(flattened)
        new_img = self.recreate_image(kmeans.cluster_centers_, labels, width, height)
        return new_img, kmeans.cluster_centers_

    def recreate_image(self, codebook, labels, width, height):
        vfunc = lambda x: codebook[labels[x]]
        out = vfunc(np.arange(width * height))
        return np.resize(out, (width, height, codebook.shape[1]))

# Configurações da barra lateral
st.sidebar.title("CLUBE DE ARTES PLÁSTICAS")

# Separador
st.sidebar.write("---")

# Seção de Informações do Autor
st.sidebar.header("Sketching and concept development da paleta de cor")
st.sidebar.image("clube.png", use_column_width=True)

st.sidebar.write("Nome: Marcelo Claro")
st.sidebar.write("Email: marceloclaro@geomaker.org")
st.sidebar.write("WhatsApp: (88) 98158-7145")

# Separador
st.sidebar.write("---")

# Seção de Configurações
st.sidebar.header("Configurações do Aplicativo")
uploaded_file = st.sidebar.file_uploader("Escolha uma imagem para tela", type=["jpg", "png"])
nb_color = st.sidebar.slider('Escolha o número de cores para pintar', min_value=1, max_value=100, value=2, step=1)
total_ml = st.sidebar.slider('Escolha o total em ml da tinta de cada cor', min_value=1, max_value=1000, value=10, step=1)
pixel_size = st.sidebar.slider('Escolha o tamanho do pixel da pintura', min_value=500, max_value=4000, value=4000, step=100)



# ...

if st.sidebar.button('Gerar'):
    if uploaded_file is not None:
        # Abrir a imagem diretamente do arquivo carregado
        pil_image = Image.open(uploaded_file)
        if 'dpi' in pil_image.info:
            dpi = pil_image.info['dpi']
            st.write(f'Resolução da imagem: {dpi} DPI')

            # Calcula a dimensão física de um pixel
            cm_per_inch = pixel_size
            cm_per_pixel = cm_per_inch / dpi[0]  # Supõe-se que a resolução seja a mesma em ambas as direções
            st.write(f'Tamanho de cada pixel: {cm_per_pixel:.4f} centímetros')

        # Converter pil_image em uma matriz NumPy
        src = np.array(pil_image)

        canvas = Canvas(src, nb_color, pixel_size)  # Use src aqui em vez de pil_image
        result, colors, segmented_image = canvas.generate()
        
        

    # Converter imagem segmentada para np.uint8
    segmented_image = (segmented_image * 255).astype(np.uint8)

    # Agora converta de BGR para RGB
    segmented_image = cv2.cvtColor(segmented_image, cv2.COLOR_BGR2RGB)
    # Separador
    st.write("---")
    # Análise da Cor Dominante Junguiana
    cor_dominante = buscar_cor_proxima(colors[0], cores_junguianas)

    st.subheader("Análise da Cor Dominante Junguiana")
    st.write(f"A cor dominante na paleta é {cor_dominante['cor']}.")
    st.write(f"Anima/Animus: {cor_dominante['anima_animus']}")
    st.write(f"Sombra: {cor_dominante['sombra']}")
    st.write(f"Personalidade: {cor_dominante['personalidade']}")
    st.write(f"Diagnóstico: {cor_dominante['diagnostico']}")
    # Separador
    st.write("---")

    # Mostrar paleta de cores

    for i, color in enumerate(colors):
        color_block = np.ones((50, 50, 3), np.uint8) * color[::-1]  # Cores em formato BGR
        st.image(color_block, caption=f'Cor {i+1}', width=50)

        # Cálculo das proporções das cores CMYK
        r, g, b = color
        c, m, y, k = rgb_to_cmyk(r, g, b)
        c_ml, m_ml, y_ml, k_ml = calculate_ml(c, m, y, k, total_ml)

        # Calcular a área da cor na imagem segmentada
        color_area = np.count_nonzero(np.all(segmented_image == color, axis=-1))
        total_area = segmented_image.shape[0] * segmented_image.shape[1]
        color_percentage = (color_area / total_area) * 100

        
        st.write("---")
        st.subheader("Sketching and concept development da paleta de cor")
        st.write(f"""
        PALETAS DE COR PARA: {total_ml:.2f} ml.

        A cor pode ser alcançada pela combinação das cores primárias do modelo CMYK, utilizando a seguinte dosagem:

        Ciano (Azul) (C): {c_ml:.2f} ml
        Magenta (Vermelho) (M): {m_ml:.2f} ml
        Amarelo (Y): {y_ml:.2f} ml
        Preto (K): {k_ml:.2f} ml

        """)
        # Separador
        st.write("---")
        cor_proxima = buscar_cor_proxima(color, cores_junguianas)
        st.write(f"      Cor Junguiana Mais Próxima: {cor_proxima['cor']}")
        st.write(f"      Anima/Animus: {cor_proxima['anima_animus']}")
        st.write(f"      Sombra: {cor_proxima['sombra']}")
        st.write(f"      Personalidade: {cor_proxima['personalidade']}")
        st.write(f"      Diagnóstico: {cor_proxima['diagnostico']}")
        st.write("---")

    result_bytes = cv2.imencode('.jpg', result)[1].tobytes()
    st.write("Tela e Esboço")
    # Separador
    st.write("---")
    st.image(result, caption='Imagem para pintar', use_column_width=True)
    st.download_button(
        label="Baixar Imagem para pintar",
        data=result_bytes,
        file_name='result.jpg',
        mime='image/jpeg')


    segmented_image_rgb = cv2.cvtColor(segmented_image, cv2.COLOR_BGR2RGB)
    segmented_image_bytes = cv2.imencode('.jpg', segmented_image_rgb)[1].tobytes()
    # Separador
    st.write("---")
     
    st.image(segmented_image, caption='Imagem Segmentada', use_column_width=True)
    st.download_button(
        label="Baixar imagem segmentada",
        data=segmented_image_bytes,
        file_name='segmented.jpg',
        mime='image/jpeg')
