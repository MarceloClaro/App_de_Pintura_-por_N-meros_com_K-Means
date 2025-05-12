# Importando todas as coisas necessárias para o nosso programa funcionar.
# Esses são como os blocos de construção que vamos usar para fazer o nosso programa.

import numpy as np  # Esta é uma ferramenta para lidar com listas de números.
from sklearn.cluster import KMeans  # Essa é uma ferramenta que nos ajuda a encontrar grupos de coisas.
from sklearn.utils import shuffle  # Isso nos ajuda a misturar coisas.
import cv2  # Esta é uma ferramenta para trabalhar com imagens.
import streamlit as st  # Isso é o que nos permite criar a interface do nosso programa.
from PIL import Image  # Outra ferramenta para trabalhar com imagens.
import io  # Essa é uma ferramenta que nos ajuda a lidar com arquivos e dados.

cores_junguianas = {
    '1': {
        'cor': 'Preto',
        'rgb': (0, 0, 0),
        'anima_animus': 'O inconsciente profundo, o mistério, o potencial não manifesto, a Grande Mãe Terra (aspecto ctônico).',
        'sombra': 'Repressão, medo do desconhecido, negação, luto não processado, vazio existencial, instintos primordiais não integrados.',
        'personalidade': 'Enigmática, introspectiva, poderosa, séria, pode buscar profundidade ou se isolar.',
        'diagnostico': 'Pode indicar um mergulho necessário no inconsciente, luto, depressão, ou a necessidade de confrontar a própria sombra e o desconhecido.',
        'referencias': 'Interpretações baseadas nos conceitos de Sombra, Inconsciente Coletivo e simbolismo arquetípico de C.G. Jung (e.g., "O Homem e Seus Símbolos", "Arquétipos e o Inconsciente Coletivo"). O preto frequentemente simboliza o nigredo alquímico.'
    },
    '2': {
        'cor': 'Branco',
        'rgb': (255, 255, 255),
        'anima_animus': 'Pureza, totalidade, o Self não diferenciado, potencialidade, transcendência, clareza espiritual.',
        'sombra': 'Frieza, vazio, negação da vida instintiva e da "sujeira" terrena, perfeccionismo estéril, isolamento idealista.',
        'personalidade': 'Idealista, busca clareza e perfeição, pode ser espiritualizada ou distante das realidades mundanas.',
        'diagnostico': 'Pode sugerir busca por paz e pureza, um novo começo, ou um distanciamento excessivo da realidade e das emoções "negativas".',
        'referencias': 'Simbolismo do Self, individuação e o albedo alquímico. Ver obras de C.G. Jung sobre o Self e a totalidade psíquica.'
    },
    '3': {
        'cor': 'Vermelho (Puro)',
        'rgb': (255, 0, 0),
        'anima_animus': 'Energia vital (libido), paixão, ação, coragem, o princípio masculino ativo (Eros dinâmico).',
        'sombra': 'Raiva, agressividade descontrolada, impulsividade destrutiva, perigo, luxúria, inflamação.',
        'personalidade': 'Extrovertida, assertiva, energética, competitiva, apaixonada, pode ser impulsiva.',
        'diagnostico': 'Excesso pode indicar stress, raiva contida, necessidade de ação e expressão da vitalidade, ou inflamação física/psíquica.',
        'referencias': 'Associações com a função sentimento extrovertido, libido e o arquétipo do Guerreiro. O rubedo alquímico. Ver "Tipos Psicológicos" de Jung.'
    },
    '4': {
        'cor': 'Azul (Cobalto)',
        'rgb': (0, 71, 171),
        'anima_animus': 'Espiritualidade, pensamento (Logos), introspecção, verdade, lealdade, o feminino receptivo, profundidade psíquica.',
        'sombra': 'Frieza emocional, distanciamento, depressão, melancolia, rigidez de pensamento, dogmatismo.',
        'personalidade': 'Calma, ponderada, intelectual, leal, conservadora, busca profundidade e significado.',
        'diagnostico': 'Pode indicar necessidade de introspecção, busca por verdade e calma, ou um período de tristeza e isolamento.',
        'referencias': 'Associações com a função pensamento introvertido, o arquétipo do Sábio, e o simbolismo do céu e do mar profundo. Ver "Tipos Psicológicos" de Jung.'
    },
    '5': {
        'cor': 'Verde (Esmeralda)',
        'rgb': (80, 200, 120),
        'anima_animus': 'Natureza, crescimento, cura, fertilidade, esperança, sentimento (Eros conectado à natureza), renovação.',
        'sombra': 'Inveja, ciúme, imaturidade, estagnação, possessividade, engano (como a serpente no jardim).',
        'personalidade': 'Equilibrada, harmoniosa, compassiva, generosa, prática, conectada com o crescimento.',
        'diagnostico': 'Pode indicar necessidade de renovação, contato com a natureza, cura física ou emocional, ou questões de crescimento pessoal e inveja.',
        'referencias': 'Simbolismo da natureza, o arquétipo da Grande Mãe (aspecto nutritivo), e a função sentimento. Ver estudos sobre simbolismo da natureza na psicologia analítica.'
    },
    '6': {
        'cor': 'Amarelo (Limão)',
        'rgb': (255, 247, 0),
        'anima_animus': 'Intelecto, intuição (como insight súbito), otimismo, alegria, extroversão, inspiração, clareza mental.',
        'sombra': 'Covardia, superficialidade, traição (como Judas), ansiedade, crítica excessiva, racionalização excessiva.',
        'personalidade': 'Comunicativa, alegre, curiosa, criativa, espontânea, pode ser volátil.',
        'diagnostico': 'Pode indicar necessidade de clareza mental, expressão de alegria e otimismo, ou sobrecarga de estímulos e ansiedade.',
        'referencias': 'Associações com a função intuição extrovertida e o simbolismo solar (aspecto de iluminação). Ver "Tipos Psicológicos" de Jung.'
    },
    '7': {
        'cor': 'Laranja',
        'rgb': (255, 165, 0),
        'anima_animus': 'Criatividade, entusiasmo, alegria social, vitalidade extrovertida, prazer sensorial, aventura.',
        'sombra': 'Superficialidade, dependência de aprovação, excesso de indulgência, falta de seriedade, exibicionismo.',
        'personalidade': 'Otimista, sociável, aventureiro, enérgico, busca prazer e interação.',
        'diagnostico': 'Pode indicar necessidade de expressão criativa, socialização, busca por prazer e alegria, ou uma fase de transição e exploração.',
        'referencias': 'Combinação de energias do vermelho (ação) e amarelo (alegria/intelecto). Simbolismo da função sensação extrovertida. Ver "Tipos Psicológicos" de Jung.'
    },
    '8': {
        'cor': 'Roxo/Violeta',
        'rgb': (128, 0, 128),
        'anima_animus': 'Espiritualidade elevada, intuição, transformação, nobreza, conexão com o inconsciente profundo e o mistério.',
        'sombra': 'Luto não resolvido, melancolia, arrogância espiritual, escapismo, irrealismo, autopunição.',
        'personalidade': 'Intuitiva, artística, sensível, misteriosa, busca significado e propósito, pode ser um tanto isolada.',
        'diagnostico': 'Pode indicar um período de introspecção profunda, busca espiritual, necessidade de integrar experiências transformadoras, ou luto.',
        'referencias': 'Simbolismo da transformação, espiritualidade e o transcendente. Conexão com o arquétipo do Mago ou da Sacerdotisa. Ver obras sobre simbolismo e alquimia.'
    },
    '9': {
        'cor': 'Rosa (Claro)',
        'rgb': (255, 182, 193),
        'anima_animus': 'Amor incondicional, compaixão, cuidado, ternura, receptividade, inocência, o feminino jovem.',
        'sombra': 'Imaturidade emocional, fragilidade excessiva, sentimentalismo, necessidade de resgate, ingenuidade perigosa.',
        'personalidade': 'Gentil, afetuosa, carinhosa, empática, pode ser idealista e um pouco ingênua.',
        'diagnostico': 'Pode indicar necessidade de amor próprio e cuidado, cura emocional, ou o desenvolvimento de qualidades mais suaves e receptivas.',
        'referencias': 'Simbolismo do amor, cuidado e o arquétipo da Donzela ou da Criança Divina (aspecto vulnerável e puro). Associado à função sentimento.'
    },
    '10': {
        'cor': 'Marrom (Terra)',
        'rgb': (139, 69, 19),
        'anima_animus': 'Conexão com a terra, estabilidade, segurança, simplicidade, raízes, o corpo físico, praticidade.',
        'sombra': 'Estagnação, teimosia, materialismo excessivo, falta de aspiração, peso, sujeira (no sentido de não elaborado).',
        'personalidade': 'Prática, confiável, sólida, aprecia o conforto e a tradição, pés no chão.',
        'diagnostico': 'Pode indicar necessidade de aterramento (grounding), segurança material, ou uma fase de consolidação e praticidade, ou estagnação.',
        'referencias': 'Simbolismo da terra, o corpo e a função sensação introvertida. Ver "Tipos Psicológicos" e discussões sobre o aspecto ctônico.'
    },
    '11': {
        'cor': 'Cinza (Médio)',
        'rgb': (128, 128, 128),
        'anima_animus': 'Neutralidade, equilíbrio, objetividade, maturidade, contenção, o "entre-mundos".',
        'sombra': 'Indiferença, falta de compromisso, depressão, medo da vida, repressão emocional, estagnação, falta de cor.',
        'personalidade': 'Reservada, analítica, prudente, pode ser indecisa ou imparcial, busca moderação.',
        'diagnostico': 'Pode indicar um período de transição, necessidade de distanciamento para avaliação, um estado de exaustão emocional, ou depressão.',
        'referencias': 'Simbolismo da neutralidade, da sombra e da transição. Pode representar a conjunção dos opostos de forma não diferenciada.'
    },
    '12': {
        'cor': 'Dourado',
        'rgb': (255, 215, 0),
        'anima_animus': 'Iluminação, sabedoria, o Self realizado, valor, prosperidade, poder espiritual, o Sol.',
        'sombra': 'Ostentação, materialismo, ego inflado (inflação psíquica), corrupção pelo poder, falsidade, ganância.',
        'personalidade': 'Carismática, confiante, generosa, busca excelência e reconhecimento, magnânima.',
        'diagnostico': 'Pode indicar um período de grande realização e autoconfiança, ou a necessidade de reconhecer o próprio valor e brilho; cuidado com a inflação.',
        'referencias': 'Simbolismo solar, o Self, o "ouro alquímico" (Lapis Philosophorum). Ver obras de Jung sobre alquimia e o processo de individuação.'
    },
    '13': {
        'cor': 'Prateado',
        'rgb': (192, 192, 192),
        'anima_animus': 'Intuição, reflexão, o feminino arquetípico (Lua), clareza mental sutil, modernidade, valor intrínseco.',
        'sombra': 'Frieza, distanciamento emocional, ilusão, indecisão, superficialidade elegante, inconstância.',
        'personalidade': 'Intuitiva, elegante, sofisticada, busca harmonia e paz interior, pode ser adaptável.',
        'diagnostico': 'Pode indicar necessidade de introspecção, conexão com a intuição e o feminino, ou um período de purificação e clareza.',
        'referencias': 'Simbolismo lunar, Anima, o inconsciente. Associado à intuição e ao mundo dos sonhos e reflexos.'
    },
    '14': {
        'cor': 'Turquesa/Ciano',
        'rgb': (64, 224, 208),
        'anima_animus': 'Cura emocional, comunicação clara (especialmente do coração), proteção, individualidade, tranquilidade expressiva.',
        'sombra': 'Dificuldade em expressar sentimentos, isolamento autoimposto, frieza defensiva, superficialidade na comunicação.',
        'personalidade': 'Calma, comunicativa, criativa, independente, busca clareza e expressão autêntica, curativa.',
        'diagnostico': 'Pode indicar necessidade de cura emocional, melhoria na comunicação (falar a sua verdade), ou fortalecimento da individualidade e autoconfiança.',
        'referencias': 'Combinação de azul (pensamento/calma) e verde (sentimento/cura). Simbolismo da comunicação e da autoexpressão curativa.'
    },
    '15': {
        'cor': 'Magenta',
        'rgb': (255, 0, 255),
        'anima_animus': 'Espiritualidade prática, harmonia universal, compaixão não sentimental, transformação interior, gratidão.',
        'sombra': 'Excentricidade, não praticidade, sentimento de superioridade espiritual, desequilíbrio emocional.',
        'personalidade': 'Inovadora, artística, compassiva, busca equilíbrio entre o espiritual e o material, inconformista.',
        'diagnostico': 'Pode indicar um período de grande insight espiritual, necessidade de alinhar ações com valores elevados, ou de expressar compaixão de forma ativa.',
        'referencias': 'Cor não espectral, simboliza a união de opostos (vermelho e violeta). Associada à transformação e à espiritualidade que transcende o comum.'
    },
    '16': {
        'cor': 'Índigo',
        'rgb': (75, 0, 130),
        'anima_animus': 'Intuição profunda (terceiro olho), sabedoria interior, percepção além do comum, autoridade espiritual, integridade.',
        'sombra': 'Medo do desconhecido, fanatismo, isolamento por se sentir incompreendido, depressão por excesso de percepção, dogmatismo.',
        'personalidade': 'Introspectiva, sábia, perceptiva, busca conhecimento profundo e verdade, pode ser vista como "diferente".',
        'diagnostico': 'Pode indicar uma forte conexão com o inconsciente, necessidade de confiar na intuição, ou um período de busca por respostas existenciais e integridade.',
        'referencias': 'Associado à intuição profunda e à percepção psíquica. Ver estudos sobre estados alterados de consciência e simbolismo do "terceiro olho".'
    },
    '17': {
        'cor': 'Verde Oliva',
        'rgb': (128, 128, 0),
        'anima_animus': 'Paz, sabedoria prática, conexão com a natureza de forma madura, esperança resiliente, estratégia.',
        'sombra': 'Amargura, ressentimento, engano, estagnação disfarçada de paz, covardia.',
        'personalidade': 'Diplomática, observadora, perspicaz, valoriza a harmonia e a estratégia, resiliente.',
        'diagnostico': 'Pode indicar necessidade de resolução de conflitos (internos ou externos), busca por paz interior duradoura, ou aplicação da sabedoria de forma prática.',
        'referencias': 'Simbolismo da paz (ramo de oliveira) e da sabedoria terrena. Uma mistura de verde (natureza) e amarelo/marrom (terra/intelecto).'
    },
    '18': {
        'cor': 'Verde Limão (Chartreuse)',
        'rgb': (127, 255, 0),
        'anima_animus': 'Juventude, vigor, otimismo efervescente, clareza mental e emocional, novidade, espontaneidade.',
        'sombra': 'Imaturidade, inveja aguda, acidez, irritabilidade, ansiedade por novidade.',
        'personalidade': 'Energética, alegre, comunicativa, pode ser um pouco impulsiva ou superficial, inovadora.',
        'diagnostico': 'Pode indicar necessidade de renovação, leveza, ou um alerta para não ser excessivamente crítico, invejoso ou ansioso por constante mudança.',
        'referencias': 'Combinação de verde (crescimento) e amarelo (alegria/intelecto). Simboliza energia nova e vibrante.'
    },
    '19': {
        'cor': 'Azul Celeste/Claro',
        'rgb': (173, 216, 230),
        'anima_animus': 'Paz, tranquilidade, serenidade, comunicação suave, esperança e proteção espiritual, o céu.',
        'sombra': 'Passividade, ingenuidade, frieza distante, dificuldade em impor limites, tristeza suave.',
        'personalidade': 'Calma, sonhadora, idealista, busca harmonia e entendimento, gentil.',
        'diagnostico': 'Pode indicar necessidade de paz interior, relaxamento, ou desenvolvimento de uma comunicação mais assertiva e suave, ou um toque de melancolia.',
        'referencias': 'Simbolismo do céu, tranquilidade e espiritualidade serena. Associado à função pensamento de forma mais leve.'
    },
    '20': {
        'cor': 'Azul Marinho',
        'rgb': (0, 0, 128),
        'anima_animus': 'Autoridade, responsabilidade, profundidade de conhecimento, confiança, ordem, o mar profundo.',
        'sombra': 'Rigidez, conservadorismo excessivo, autoritarismo, melancolia profunda, repressão, medo da desordem.',
        'personalidade': 'Séria, confiável, organizada, leal, com forte senso de dever, introspectiva.',
        'diagnostico': 'Pode indicar necessidade de estrutura, disciplina, ou um período de introspecção séria e tomada de decisões importantes; cuidado com a rigidez.',
        'referencias': 'Simbolismo da autoridade, profundidade e o inconsciente (como o mar). Associado ao arquétipo do Rei ou do Juiz.'
    },
    '21': {
        'cor': 'Bege',
        'rgb': (245, 245, 220),
        'anima_animus': 'Simplicidade, conforto, neutralidade calma, praticidade e modéstia, o básico.',
        'sombra': 'Falta de opinião, tédio, conformismo, falta de vitalidade, invisibilidade.',
        'personalidade': 'Calma, conservadora, confiável, aprecia a estabilidade e o básico, discreta.',
        'diagnostico': 'Pode indicar necessidade de simplicidade, redução de stress, ou um desejo por um ambiente neutro e acolhedor; atenção para não cair no tédio.',
        'referencias': 'Simbolismo da neutralidade e do conforto básico. Uma cor "não declarativa", que pode ser um pano de fundo para outras energias.'
    },
    '22': {
        'cor': 'Creme',
        'rgb': (255, 253, 208),
        'anima_animus': 'Suavidade, pureza com calor, conforto, elegância discreta, receptividade, nutrição.',
        'sombra': 'Passividade excessiva, falta de assertividade, pode ser visto como sem graça ou insípido.',
        'personalidade': 'Gentil, calma, apreciadora do conforto e da tradição, com um toque de sofisticação, acolhedora.',
        'diagnostico': 'Pode indicar necessidade de nutrição emocional, um ambiente tranquilo, ou o desejo de expressar elegância de forma sutil e acolhedora.',
        'referencias': 'Um branco "aquecido", simbolizando pureza com um toque de humanidade e conforto. Associado à nutrição e ao cuidado.'
    },
    '23': {
        'cor': 'Salmão',
        'rgb': (250, 128, 114),
        'anima_animus': 'Saúde, felicidade, aceitação do corpo, compaixão e otimismo gentil, fluxo da vida.',
        'sombra': 'Dependência emocional, superficialidade nas relações, busca por aprovação constante, medo da solidão.',
        'personalidade': 'Amigável, sociável, otimista, busca harmonia nos relacionamentos, cuidadora.',
        'diagnostico': 'Pode indicar foco na saúde e bem-estar (físico e emocional), necessidade de conexões sociais positivas, ou cura de questões de autoimagem.',
        'referencias': 'Combinação de rosa (compaixão) e laranja (alegria social). Simboliza bem-estar e conexão interpessoal saudável.'
    },
    '24': {
        'cor': 'Lavanda',
        'rgb': (230, 230, 250),
        'anima_animus': 'Espiritualidade delicada, intuição suave, paz interior, cura e purificação, nostalgia gentil.',
        'sombra': 'Nostalgia excessiva, fragilidade, escapismo para um mundo de fantasia, melancolia suave.',
        'personalidade': 'Sensível, imaginativa, calma, busca beleza e tranquilidade, um pouco etérea.',
        'diagnostico': 'Pode indicar necessidade de relaxamento, conexão com o lado mais sutil da vida, ou um período de cura e introspecção suave; atenção ao escapismo.',
        'referencias': 'Um violeta suavizado com branco. Simboliza espiritualidade gentil, cura e intuição delicada.'
    },
    '25': {
        'cor': 'Bordô/Vinho',
        'rgb': (128, 0, 32),
        'anima_animus': 'Paixão madura, poder controlado, sofisticação, ambição, força interior, riqueza interior.',
        'sombra': 'Raiva reprimida, crueldade, arrogância, manipulação, luxúria controladora.',
        'personalidade': 'Forte, determinada, elegante, ambiciosa, pode ser introspectiva e intensa, líder.',
        'diagnostico': 'Pode indicar um período de grande força pessoal, necessidade de expressar poder de forma construtiva, ou lidar com emoções intensas e profundas.',
        'referencias': 'Um vermelho escurecido, simbolizando paixão internalizada, poder e sofisticação. Pode ter conotações de realeza e autoridade.'
    },
    '26': {
        'cor': 'Carvão (Cinza Escuro)',
        'rgb': (54, 69, 79),
        'anima_animus': 'Força, resiliência, mistério, proteção, sofisticação discreta, a sombra integrada.',
        'sombra': 'Depressão, pessimismo, isolamento, teimosia, negatividade, peso existencial.',
        'personalidade': 'Forte, estável, séria, pode ser misteriosa ou introspectiva, confiável.',
        'diagnostico': 'Pode indicar necessidade de introspecção, enfrentamento de desafios com força, ou um período de seriedade e foco; atenção à negatividade.',
        'referencias': 'Um preto suavizado, mantendo o mistério mas com mais solidez e menos absoluto. Simboliza a força que vem da integração da sombra.'
    },
    '27': {
        'cor': 'Terracota',
        'rgb': (226, 114, 91),
        'anima_animus': 'Conexão com as raízes ancestrais, calor terreno, criatividade manual, simplicidade rústica, fertilidade da terra.',
        'sombra': 'Apego excessivo ao passado, resistência à mudança, teimosia, rusticidade excessiva.',
        'personalidade': 'Acolhedora, prática, artística (especialmente manual), conectada com a natureza e o tangível.',
        'diagnostico': 'Pode indicar necessidade de se conectar com a terra e as raízes, valorizar o simples, ou expressar criatividade de forma tangível.',
        'referencias': 'Cor da argila cozida, simboliza a conexão com a terra, o artesanato e a ancestralidade. Uma mistura de marrom e laranja.'
    },
    '28': {
        'cor': 'Mostarda (Amarelo Ocre)',
        'rgb': (222, 170, 14),
        'anima_animus': 'Intelecto maduro, sabedoria prática derivada da experiência, otimismo cauteloso, discernimento.',
        'sombra': 'Cinismo, amargura, inveja disfarçada, crítica destrutiva, teimosia intelectual.',
        'personalidade': 'Inteligente, observadora, com um humor particular, pode ser um pouco excêntrica ou antiquada.',
        'diagnostico': 'Pode indicar um período de reflexão sobre experiências passadas, aplicação da sabedoria, ou a necessidade de evitar o cinismo e a amargura.',
        'referencias': 'Um amarelo terroso, simbolizando um intelecto que foi temperado pela experiência. Menos brilhante que o amarelo limão, mais ponderado.'
    },
    '29': {
        'cor': 'Coral',
        'rgb': (255, 127, 80),
        'anima_animus': 'Energia social, alegria, vitalidade, otimismo, criatividade expressiva e comunitária, empatia.',
        'sombra': 'Necessidade excessiva de atenção, superficialidade, impulsividade em grupo, fofoca.',
        'personalidade': 'Extrovertida, entusiasmada, amigável, gosta de estar em grupo e compartilhar, calorosa.',
        'diagnostico': 'Pode indicar necessidade de interação social, expressão de alegria, ou participação em atividades comunitárias e colaborativas.',
        'referencias': 'Mistura de laranja e rosa, simboliza a alegria da conexão social e a vitalidade empática. Associado ao calor humano.'
    },
    '30': {
        'cor': 'Verde Água (Menta Claro)',
        'rgb': (152, 251, 152),
        'anima_animus': 'Renovação suave, clareza emocional, frescor, cura e tranquilidade mental, otimismo gentil.',
        'sombra': 'Frieza emocional disfarçada de calma, superficialidade, dificuldade em aprofundar vínculos, ingenuidade.',
        'personalidade': 'Calma, refrescante, otimista, busca harmonia e bem-estar, diplomática.',
        'diagnostico': 'Pode indicar necessidade de limpeza emocional, clareza mental, ou um período de renovação e alívio do estresse; buscar profundidade.',
        'referencias': 'Um verde claro e azulado, simbolizando frescor, cura suave e clareza. Associado à renovação e à tranquilidade.'
    }
}

def rgb_to_cmyk(r_norm, g_norm, b_norm): # Espera r,g,b normalizados (0-1)
    r_norm = max(0.0, min(1.0, r_norm))
    g_norm = max(0.0, min(1.0, g_norm))
    b_norm = max(0.0, min(1.0, b_norm))

    if (r_norm == 0) and (g_norm == 0) and (b_norm == 0): # Preto
        return 0.0, 0.0, 0.0, 1.0
    if (r_norm == 1) and (g_norm == 1) and (b_norm == 1): # Branco
        return 0.0, 0.0, 0.0, 0.0

    c = 1.0 - r_norm
    m = 1.0 - g_norm
    y = 1.0 - b_norm

    min_cmy = min(c, m, y)
    
    denominator = 1.0 - min_cmy
    if abs(denominator) < 1e-9: 
        if r_norm == 0 and g_norm == 0 and b_norm == 0: 
            return 0.0, 0.0, 0.0, 1.0
        else: 
            k_val = min_cmy 
            return 0.0,0.0,0.0, k_val

    c_final = (c - min_cmy) / denominator
    m_final = (m - min_cmy) / denominator
    y_final = (y - min_cmy) / denominator
    k_final = min_cmy 

    return c_final, m_final, y_final, k_final

def calculate_ml_with_white(r_norm, g_norm, b_norm, total_ml_target):
    r_norm = max(0.0, min(1.0, r_norm))
    g_norm = max(0.0, min(1.0, g_norm))
    b_norm = max(0.0, min(1.0, b_norm))

    white_proportion_in_rgb = min(r_norm, g_norm, b_norm)
    white_ml = white_proportion_in_rgb * total_ml_target
    colored_pigment_total_ml = total_ml_target - white_ml

    if colored_pigment_total_ml < 1e-5 : 
        return 0.0, 0.0, 0.0, 0.0, total_ml_target

    c_pigment_prop, m_pigment_prop, y_pigment_prop, k_pigment_prop = rgb_to_cmyk(r_norm, g_norm, b_norm)

    if r_norm == 1.0 and g_norm == 1.0 and b_norm == 1.0:
        return 0.0, 0.0, 0.0, 0.0, total_ml_target

    sum_cmyk_proportions = c_pigment_prop + m_pigment_prop + y_pigment_prop + k_pigment_prop

    if abs(sum_cmyk_proportions) < 1e-5:
        return 0.0, 0.0, 0.0, 0.0, total_ml_target
    else:
        c_ml = (c_pigment_prop / sum_cmyk_proportions) * colored_pigment_total_ml
        m_ml = (m_pigment_prop / sum_cmyk_proportions) * colored_pigment_total_ml
        y_ml = (y_pigment_prop / sum_cmyk_proportions) * colored_pigment_total_ml
        k_ml = (k_pigment_prop / sum_cmyk_proportions) * colored_pigment_total_ml
        
    calculated_colored_ml = c_ml + m_ml + y_ml + k_ml
    white_ml = total_ml_target - calculated_colored_ml 

    c_ml = max(0.0, c_ml)
    m_ml = max(0.0, m_ml)
    y_ml = max(0.0, y_ml)
    k_ml = max(0.0, k_ml)
    white_ml = max(0.0, white_ml)
    
    final_sum = c_ml + m_ml + y_ml + k_ml + white_ml
    if abs(final_sum - total_ml_target) > 1e-5 and final_sum > 1e-5 :
        scale_factor = total_ml_target / final_sum
        c_ml *= scale_factor
        m_ml *= scale_factor
        y_ml *= scale_factor
        k_ml *= scale_factor
        white_ml *= scale_factor

    return c_ml, m_ml, y_ml, k_ml, white_ml

def buscar_cor_proxima(rgb_query, cores_junguianas_dict):
    if max(rgb_query) <= 1.0: 
        rgb_query_255 = tuple(int(c * 255) for c in rgb_query)
    else:
        rgb_query_255 = tuple(int(c) for c in rgb_query)

    min_distancia = float('inf')
    cor_mais_proxima_info = None
    
    if not cores_junguianas_dict:
        return {
            'cor': 'N/A', 'rgb': (0,0,0), 'anima_animus': 'Dicionário vazio.',
            'sombra': 'Dicionário vazio.', 'personalidade': 'Dicionário vazio.',
            'diagnostico': 'Dicionário de cores Junguianas está vazio.',
            'referencias': ''
        }

    for key, cor_data in cores_junguianas_dict.items():
        cor_junguiana_rgb = cor_data['rgb']
        distancia = np.sqrt(np.sum((np.array(rgb_query_255) - np.array(cor_junguiana_rgb)) ** 2))
        if distancia < min_distancia:
            min_distancia = distancia
            cor_mais_proxima_info = cor_data
            
    if cor_mais_proxima_info is None and cores_junguianas_dict: 
        return cores_junguianas_dict[next(iter(cores_junguianas_dict))]

    return cor_mais_proxima_info

class Canvas():
    def __init__(self, src_rgb, nb_color, target_dimension_px):
        self.src_rgb = src_rgb 
        self.nb_color = nb_color
        self.target_dimension_px = target_dimension_px
        self.colormap_rgb_0_255 = [] 

    def generate(self):
        im_source_resized_rgb = self.resize() 
        clean_img_rgb = self.cleaning(im_source_resized_rgb) 
        
        clean_img_norm_rgb = np.array(clean_img_rgb, dtype=np.float32) / 255.0 
        
        quantified_image_norm_rgb, colors_palette_norm_rgb = self.quantification(clean_img_norm_rgb)
        
        quantified_image_uint8_rgb = (quantified_image_norm_rgb * 255).astype(np.uint8) 

        canvas_paint = np.ones(quantified_image_uint8_rgb.shape[:2], dtype="uint8") * 255 

        self.colormap_rgb_0_255 = []
        if isinstance(colors_palette_norm_rgb, np.ndarray) and colors_palette_norm_rgb.shape[0] > 0:
            for ind, color_norm_rgb in enumerate(colors_palette_norm_rgb):
                self.colormap_rgb_0_255.append([int(c * 255) for c in color_norm_rgb])
                
                color_uint8_rgb_val = (color_norm_rgb * 255).astype(np.uint8)
                mask = cv2.inRange(quantified_image_uint8_rgb, color_uint8_rgb_val, color_uint8_rgb_val)
                contours, _ = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

                for contour in contours:
                    if cv2.contourArea(contour) > 100: 
                        cv2.drawContours(canvas_paint, [contour], -1, (0, 0, 0), 1) 
                        M = cv2.moments(contour)
                        if M["m00"] != 0:
                            txt_x = int(M["m10"] / M["m00"])
                            txt_y = int(M["m01"] / M["m00"])
                            cv2.putText(canvas_paint, '{:d}'.format(ind + 1), (txt_x, txt_y),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1) 
        
        return canvas_paint, colors_palette_norm_rgb, quantified_image_uint8_rgb

    def resize(self):
        (height, width) = self.src_rgb.shape[:2]
        if width == 0 or height == 0: 
            st.warning("Imagem de entrada parece estar vazia ou corrompida.")
            return np.zeros((100,100,3), dtype=self.src_rgb.dtype) 

        if height > width:
            new_width = int(width * self.target_dimension_px / float(height))
            dim = (max(1, new_width), self.target_dimension_px) 
        else: 
            new_height = int(height * self.target_dimension_px / float(width))
            dim = (self.target_dimension_px, max(1, new_height)) 
        
        if dim[0] <= 0 or dim[1] <= 0:
             dim = (100,100)

        return cv2.resize(self.src_rgb, dim, interpolation=cv2.INTER_AREA)

    def cleaning(self, picture_rgb_uint8):
        denoised_rgb = cv2.fastNlMeansDenoisingColored(picture_rgb_uint8, None, 10, 10, 7, 21)
        kernel = np.ones((5, 5), np.uint8)
        img_erosion_rgb = cv2.erode(denoised_rgb, kernel, iterations=1)
        img_dilation_rgb = cv2.dilate(img_erosion_rgb, kernel, iterations=1)
        return img_dilation_rgb

    def quantification(self, picture_norm_rgb_float32):
        width, height, depth = picture_norm_rgb_float32.shape
        if width * height == 0: 
            return picture_norm_rgb_float32, np.array([])

        flattened_rgb = np.reshape(picture_norm_rgb_float32, (width * height, depth))
        
        sample_size = min(1000, flattened_rgb.shape[0]) 
        if sample_size == 0: 
            return picture_norm_rgb_float32, np.array([])

        sample_rgb = shuffle(flattened_rgb, random_state=42, n_samples=sample_size)
        
        actual_nb_color = min(self.nb_color, sample_rgb.shape[0])
        if actual_nb_color < 1: 
            if sample_rgb.shape[0] > 0: 
                return self.recreate_image(sample_rgb[0:1], np.zeros(flattened_rgb.shape[0], dtype=int), width, height), sample_rgb[0:1]
            return picture_norm_rgb_float32, np.array([])

        kmeans = KMeans(n_clusters=actual_nb_color, random_state=42, n_init='auto').fit(sample_rgb)
        labels = kmeans.predict(flattened_rgb)
        
        new_img_norm_rgb = self.recreate_image(kmeans.cluster_centers_, labels, width, height) 
        return new_img_norm_rgb, kmeans.cluster_centers_ 

    def recreate_image(self, codebook_norm_rgb, labels, width, height):
        d = codebook_norm_rgb.shape[1]
        image = np.zeros((width * height, d), dtype=np.float32) 
        for i in range(width * height):
            image[i] = codebook_norm_rgb[labels[i]]
        return np.resize(image, (width, height, d))

# --- Interface Streamlit ---
st.set_page_config(layout="wide") 

st.sidebar.title("🖌️ Criador de Tela para Pintar")
st.sidebar.write("---")

st.sidebar.header("ℹ️ Informações do Autor")
try:
    st.sidebar.image("clube.png", use_container_width=True)
except Exception:
    st.sidebar.caption("Logo 'clube.png' não encontrado.") 
st.sidebar.write("Nome: Marcelo Claro")
st.sidebar.write("Email: marceloclaro@geomaker.org")
st.sidebar.write("WhatsApp: (88) 98158-7145")

st.sidebar.write("---")

st.sidebar.header("⚙️ Configurações da Aplicação")
uploaded_file = st.sidebar.file_uploader("Escolha uma imagem", type=["jpg", "png", "jpeg"])
nb_color_slider = st.sidebar.slider('Número de cores na paleta', min_value=1, max_value=30, value=5, step=1) 
total_ml_slider = st.sidebar.slider('Total em ml da tinta (por cor)', min_value=10, max_value=1000, value=50, step=10)
target_dimension_slider = st.sidebar.slider(
    'Dimensão alvo da imagem (pixels)', 
    min_value=300, max_value=2000, value=800, step=50,
    help="A maior dimensão (largura ou altura) da imagem será ajustada para este valor, mantendo a proporção."
)

if st.sidebar.button('🎨 Gerar Paleta e Tela'):
    if uploaded_file is not None:
        try:
            pil_image = Image.open(uploaded_file)

            col1_orig, col2_proc = st.columns(2)

            with col1_orig:
                st.subheader("🖼️ Imagem Original")
                st.image(pil_image, caption=f'Original: {uploaded_file.name}', use_container_width=True)

                if 'dpi' in pil_image.info:
                    dpi = pil_image.info['dpi']
                    st.write(f"Resolução: {dpi[0]:.0f}x{dpi[1]:.0f} DPI")
                    cm_per_inch = 2.54
                    if dpi[0] > 0: st.write(f"Tam. pixel X: {cm_per_inch / dpi[0]:.4f} cm")
                    if dpi[1] > 0: st.write(f"Tam. pixel Y: {cm_per_inch / dpi[1]:.4f} cm")
                else:
                    st.write("Info DPI não encontrada.")
                st.write(f"Dimensões: {pil_image.width}px x {pil_image.height}px")
            
            with st.spinner('Processando imagem... Por favor, aguarde.'):
                pil_image_rgb = pil_image.convert('RGB')
                src_np_rgb = np.array(pil_image_rgb) 

                canvas_obj = Canvas(src_np_rgb, nb_color_slider, target_dimension_slider)
                result_paint_screen, colors_palette_norm_rgb, segmented_image_uint8_rgb = canvas_obj.generate()
            
            with col2_proc:
                st.subheader("🎨 Imagem Segmentada")
                st.image(segmented_image_uint8_rgb, caption='Cores Quantizadas', use_container_width=True)
                
                _, segmented_buffer = cv2.imencode('.png', cv2.cvtColor(segmented_image_uint8_rgb, cv2.COLOR_RGB2BGR))
                st.download_button(
                    label="📥 Baixar Segmentada (.png)", data=segmented_buffer.tobytes(),
                    file_name=f'segmentada_{uploaded_file.name}.png', mime='image/png'
                )
                st.write("---")
                st.subheader("🖌️ Tela para Pintar")
                st.image(result_paint_screen, caption='Numerada para Pintar', use_container_width=True)
                _, result_buffer = cv2.imencode('.png', result_paint_screen)
                st.download_button(
                    label="📥 Baixar Tela para Pintar (.png)", data=result_buffer.tobytes(),
                    file_name=f'tela_pintar_{uploaded_file.name}.png', mime='image/png'
                )
            
            st.write("---")
            st.subheader("🌈 Paleta de Cores Gerada e Análise")

            if not isinstance(colors_palette_norm_rgb, np.ndarray) or colors_palette_norm_rgb.shape[0] == 0:
                st.warning("Nenhuma paleta de cores foi gerada. Tente com outra imagem ou configurações.")
            else:
                cor_representativa_norm_rgb = colors_palette_norm_rgb[0]
                cor_jung_representativa = buscar_cor_proxima(cor_representativa_norm_rgb, cores_junguianas)
                
                if cor_jung_representativa and cor_jung_representativa['cor'] != 'N/A':
                    expander_title = f"💡 Análise Junguiana da Cor Representativa da Paleta: {cor_jung_representativa['cor']}"
                    with st.expander(expander_title):
                        st.write(f"**Anima/Animus:** {cor_jung_representativa['anima_animus']}")
                        st.write(f"**Sombra:** {cor_jung_representativa['sombra']}")
                        st.write(f"**Personalidade:** {cor_jung_representativa['personalidade']}")
                        st.write(f"**Diagnóstico:** {cor_jung_representativa['diagnostico']}")
                        if 'referencias' in cor_jung_representativa and cor_jung_representativa['referencias']:
                            st.markdown("**Pistas para Estudo:**")
                            st.caption(cor_jung_representativa['referencias'])
                else:
                    st.caption("Análise Junguiana para a cor representativa não disponível.")
                
                st.markdown("### Detalhes das Cores da Paleta:")

                for i, color_norm_rgb_item in enumerate(colors_palette_norm_rgb):
                    color_uint8_rgb_item = [int(c * 255) for c in color_norm_rgb_item]
                    
                    st.markdown(f"---") 
                    
                    col_img, col_info = st.columns([1, 3])

                    with col_img:
                        st.markdown(f"##### Cor {i+1}")
                        color_block_display = np.full((80, 80, 3), color_uint8_rgb_item, dtype=np.uint8)
                        st.image(color_block_display, caption=f"RGB: {tuple(color_uint8_rgb_item)}", width=80)

                    with col_info:
                        r_norm, g_norm, b_norm = color_norm_rgb_item[0], color_norm_rgb_item[1], color_norm_rgb_item[2]
                        c_ml, m_ml, y_ml, k_ml, white_ml = calculate_ml_with_white(r_norm, g_norm, b_norm, total_ml_slider)

                        st.markdown(f"**Dosagem para {total_ml_slider}ml (incl. Branco):**")
                        st.markdown(f"""
                        - Ciano (C): {c_ml:.1f} ml
                        - Magenta (M): {m_ml:.1f} ml
                        - Amarelo (Y): {y_ml:.1f} ml
                        - Preto (K): {k_ml:.1f} ml
                        - **Branco (W): {white_ml:.1f} ml**
                        """)
                        
                        cor_jung_especifica = buscar_cor_proxima(color_norm_rgb_item, cores_junguianas)
                        if cor_jung_especifica and cor_jung_especifica['cor'] != 'N/A':
                            with st.expander(f"Análise Junguiana: {cor_jung_especifica['cor']}", expanded=False):
                                st.write(f"**Anima/Animus:** {cor_jung_especifica['anima_animus']}")
                                st.write(f"**Sombra:** {cor_jung_especifica['sombra']}")
                                st.write(f"**Personalidade:** {cor_jung_especifica['personalidade']}")
                                st.write(f"**Diagnóstico:** {cor_jung_especifica['diagnostico']}")
                                if 'referencias' in cor_jung_especifica and cor_jung_especifica['referencias']:
                                    st.markdown("**Pistas para Estudo:**")
                                    st.caption(cor_jung_especifica['referencias'])
                        else:
                            st.caption("(Análise Junguiana não disponível para esta cor)")
                st.markdown(f"---")

                # SEÇÃO: CAMADAS DE CORES PARA PINTURA
                st.subheader("🖼️ Camadas de Cores para Pintura (PNG)")
                st.caption("Cada imagem abaixo representa uma camada de cor. As áreas coloridas devem ser pintadas com a cor correspondente da paleta.")

                if isinstance(colors_palette_norm_rgb, np.ndarray) and colors_palette_norm_rgb.shape[0] > 0:
                    altura, largura, _ = segmented_image_uint8_rgb.shape 

                    for i, color_norm_rgb_item in enumerate(colors_palette_norm_rgb):
                        cor_atual_uint8_rgb = np.array([int(c * 255) for c in color_norm_rgb_item], dtype=np.uint8)

                        st.markdown(f"#### Camada para Cor {i+1}")
                        
                        mask_cor_atual = cv2.inRange(segmented_image_uint8_rgb, cor_atual_uint8_rgb, cor_atual_uint8_rgb)
                        camada_imagem_rgb = np.full((altura, largura, 3), 255, dtype=np.uint8) 
                        camada_imagem_rgb[mask_cor_atual > 0] = cor_atual_uint8_rgb
                        
                        col_camada_img, col_camada_info = st.columns([2,1])

                        with col_camada_img:
                            st.image(camada_imagem_rgb, use_container_width=True, 
                                     caption=f"Áreas para pintar com a Cor {i+1} (RGB: {tuple(cor_atual_uint8_rgb)})")

                        camada_imagem_bgr = cv2.cvtColor(camada_imagem_rgb, cv2.COLOR_RGB2BGR)
                        _, camada_buffer = cv2.imencode('.png', camada_imagem_bgr)
                        
                        with col_camada_info:
                            st.download_button(
                                label=f"📥 Baixar Camada Cor {i+1}",
                                data=camada_buffer.tobytes(),
                                file_name=f'camada_cor_{i+1}_{uploaded_file.name}.png',
                                mime='image/png',
                                key=f"download_camada_{i}" 
                            )
                            st.markdown("**Cor de Referência:**")
                            color_block_ref = np.full((50, 50, 3), cor_atual_uint8_rgb, dtype=np.uint8)
                            st.image(color_block_ref, width=50)
                        st.markdown("---") 
                else:
                    st.info("Paleta de cores não disponível para gerar camadas.")

        except Exception as e:
            st.error(f"Ocorreu um erro durante o processamento da imagem: {e}")
            st.error("Detalhes técnicos:")
            st.exception(e) 

    else:
        st.warning("Por favor, carregue uma imagem para gerar a paleta e a tela.")

else:
    st.info("👈 Ajuste as configurações na barra lateral, carregue uma imagem e clique em 'Gerar Paleta e Tela'.")
