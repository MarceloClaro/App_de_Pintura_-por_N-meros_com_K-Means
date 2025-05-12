        with st.spinner('Processando imagem... Por favor, aguarde.'):
            pil_image_rgb = pil_image.convert('RGB')
            src_np_rgb = np.array(pil_image_rgb) 
            canvas_obj = Canvas(src_np_rgb, nb_color_slider, target_dimension_slider)
            result_paint_screen, colors_palette_norm_rgb, segmented_image_uint8_rgb = canvas_obj.generate()
        
        with col2_proc:
            st.subheader("🎨 Imagem Segmentada")
            st.image(segmented_image_uint8_rgb, caption='Cores Quantizadas', use_container_width=True)
            _, segmented_buffer = cv2.imencode('.png', cv2.cvtColor(segmented_image_uint8_rgb, cv2.COLOR_RGB2BGR))
            st.download_button(label="📥 Baixar Segmentada (.png)", data=segmented_buffer.tobytes(), file_name=f'segmentada_{uploaded_file.name}.png', mime='image/png', key="download_segmented")
            st.write("---")
            st.subheader("🖌️ Tela para Pintar")
            st.image(result_paint_screen, caption='Numerada para Pintar', use_container_width=True)
            _, result_buffer = cv2.imencode('.png', result_paint_screen)
            st.download_button(label="📥 Baixar Tela para Pintar (.png)", data=result_buffer.tobytes(), file_name=f'tela_pintar_{uploaded_file.name}.png', mime='image/png', key="download_paint_screen")
        
        st.write("---")
        st.subheader("🌈 Paleta de Cores Gerada e Análise")
        if not isinstance(colors_palette_norm_rgb, np.ndarray) or colors_palette_norm_rgb.shape[0] == 0:
            st.warning("Nenhuma paleta de cores foi gerada. Tente com outra imagem ou configurações.")
        else:
            cor_representativa_norm_rgb = colors_palette_norm_rgb[0]
            cor_jung_representativa = buscar_cor_proxima(cor_representativa_norm_rgb, cores_junguianas)
            if cor_jung_representativa and cor_jung_representativa['cor'] != 'N/A':
                with st.expander(f"💡 Análise Junguiana da Cor Representativa da Paleta: {cor_jung_representativa['cor']}"):
                    st.write(f"**Anima/Animus:** {cor_jung_representativa['anima_animus']}")
                    st.write(f"**Sombra:** {cor_jung_representativa['sombra']}")
                    st.write(f"**Personalidade:** {cor_jung_representativa['personalidade']}")
                    st.write(f"**Diagnóstico:** {cor_jung_representativa['diagnostico']}")
                    if 'referencias' in cor_jung_representativa and cor_jung_representativa['referencias']:
                        st.markdown("**Pistas para Estudo:**"); st.caption(cor_jung_representativa['referencias'])
            else: st.caption("Análise Junguiana para a cor representativa não disponível.")
            
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
                    st.markdown(f"- Ciano (C): {c_ml:.1f} ml\n- Magenta (M): {m_ml:.1f} ml\n- Amarelo (Y): {y_ml:.1f} ml\n- Preto (K): {k_ml:.1f} ml\n- **Branco (W): {white_ml:.1f} ml**")
                    cor_jung_especifica =diagnostico': 'Pode indicar necessidade de introspecção, busca por verdade e calma, ou um período de tristeza e isolamento.',
    'referencias': 'Conceitos: Função Pensamento Introvertido, Logos, Arquétipo do Sábio. Obras relevantes: JUNG, C. G. *Tipos psicológicos*.'
},
'5': {
    'cor': 'Verde (Esmeralda)',
    'rgb': (80, 200, 120),
    'anima_animus': 'Natureza, crescimento, cura, fertilidade, esperança, sentimento (Eros conectado à natureza), renovação.',
    'sombra': 'Inveja, ciúme, imaturidade, estagnação, possessividade, engano (como a serpente no jardim).',
    'personalidade': 'Equilibrada, harmoniosa, compassiva, generosa, prática, conectada com o crescimento.',
    'diagnostico': 'Pode indicar necessidade de renovação, contato com a natureza, cura física ou emocional, ou questões de crescimento pessoal e inveja.',
    'referencias': 'Conceitos: Simbolismo da Natureza, Função Sentimento, Arquétipo da Grande Mãe. Obras relevantes: FRANZ, M.-L. von (obras sobre contos de fadas).'
},
'6': {
    'cor': 'Amarelo (Limão)',
    'rgb': (255, 247, 0),
    'anima_animus': 'Intelecto, intuição (como insight súbito), otimismo, alegria, extroversão, inspiração, clareza mental.',
    'sombra': 'Covardia, superficialidade, traição (como Judas), ansiedade, crítica excessiva, racionalização excessiva.',
    'personalidade': 'Comunicativa, alegre, curiosa, criativa, espontânea, pode ser volátil.',
    'diagnostico': 'Pode indicar necessidade de clareza mental, expressão de alegria e otimismo, ou sobrecarga de estímulos e ansiedade.',
    'referencias': 'Conceitos: Função Intuição Extrovertida, Simbolismo Solar, Citrinitas (Alquimia). Obras relevantes: JUNG, C. G. *Tipos psicológicos*; JUNG, C. G. *Psicologia e alquimia*.'
},
'7': {
    'cor': 'Laranja',
    'rgb': (255, 165, 0),
    'anima_animus': 'Criatividade, entusiasmo, alegria social, vitalidade extrovertida, prazer sensorial, aventura.',
    'sombra': 'Superficialidade, dependência de aprovação, excesso de indulgência, falta de seriedade, exibicionismo.',
    'personalidade': 'Otimista, sociável, aventureiro, enérgico, busca prazer e interação.',
    'diagnostico': 'Pode indicar necessidade de expressão criativa, socialização, busca por prazer e alegria, ou uma fase de transição e exploração.',
    'referencias': 'Conceitos: Função Sensação Extrovertida, Vitalidade. Obras relevantes: JUNG, C. G. *Tipos psicológicos*.'
},
'8': {
    'cor': 'Roxo/Violeta',
    'rgb': (128, 0, 128),
    'anima_animus': 'Espiritualidade elevada, intuição, transformação, nobreza, conexão com o inconsciente profundo e o mistério.',
    'sombra': 'Luto não resolvido, melancolia, arrogância espiritual, escapismo, irrealismo, autopunição.',
    'personalidade': 'Intuitiva, artística, sensível, misteriosa, busca significado e propósito, pode ser um tanto isolada.',
    'diagnostico': 'Pode indicar um período de introspecção profunda, busca espiritual, necessidade de integrar experiências transformadoras, ou luto.',
    'referencias': 'Conceitos: Transformação, Espiritualidade, Mistério. Obras relevantes: JUNG, C. G. *Psicologia e alquimia*.'
},
'9': {
    'cor': 'Rosa (Claro)',
    'rgb': (255, 182, 193),
    'anima_animus': 'Amor incondicional, compaixão, cuidado, ternura, receptividade, inocência, o feminino jovem.',
    'sombra': 'Imaturidade emocional, fragilidade excessiva, sentimentalismo, necessidade de resgate, ingenuidade perigosa.',
    'personalidade': 'Gentil, afetuosa, carinhosa, empática, pode ser idealista e um pouco ingênua.',
    'diagnostico': 'Pode indicar necessidade de amor próprio e cuidado, cura emocional, ou o desenvolvimento de qualidades mais suaves e receptivas.',
    'referencias': 'Conceitos: Anima (aspecto jovem), Função Sentimento, Compaixão.'
},
'10': {
    'cor': 'Marrom (Terra)',
    'rgb': (139, 69, 19),
    'anima_animus': 'Conexão com a terra, estabilidade, segurança, simplicidade, raízes, o corpo físico, praticidade.',
    'sombra': 'Estagnação, teimosia, materialismo excessivo, falta de aspiração, peso, sujeira (no sentido de não elaborado).',
    'personalidade': 'Prática, confiável, sólida, aprecia o conforto e a tradição, pés no chão.',
    'diagnostico': 'Pode indicar necessidade de aterramento (grounding), segurança material, ou uma fase de consolidação e praticidade, ou estagnação.',
    'referencias': 'Conceitos: Função Sensação Introvertida, Aspecto Ctônico. Obras relevantes: JUNG, C. G. *Tipos psicológicos*.'
},
'11': {
    'cor': 'Cinza (Médio)',
    'rgb': (128, 128, 128),
    'anima_animus': 'Neutralidade, equilíbrio, objetividade, maturidade, contenção, o "entre-mundos".',
    'sombra': 'Indiferença, falta de compromisso, depressão, medo da vida, repressão emocional, estagnação, falta de cor.',
    'personalidade': 'Reservada, analítica, prudente, pode ser indecisa ou imparcial, busca moderação.',
    'diagnostico': 'Pode indicar um período de transição, necessidade de distanciamento para avaliação, um estado de exaustão emocional, ou depressão.',
    'referencias': 'Conceitos: Neutralidade, Transição, Conjunção dos Opostos (não diferenciada).'
},
'12': {
    'cor': 'Dourado',
    'rgb': (255, 215, 0),
    'anima_animus': 'Iluminação, sabedoria, o Self realizado, valor, prosperidade, poder espiritual, o Sol.',
    'sombra': 'Ostentação, materialismo, ego inflado (inflação psíquica), corrupção pelo poder, falsidade, ganância.',
    'personalidade': 'Carismática, confiante, generosa, busca excelência e reconhecimento, magnânima.',
    'diagnostico': 'Pode indicar um período de grande realização e autoconfiança, ou a necessidade de reconhecer o próprio valor e brilho; cuidado com a inflação.',
    'referencias': 'Conceitos: Self, Simbolismo Solar, Ouro Alquímico. Obras relevantes: JUNG, C. G. *Psicologia e alquimia*; JUNG, C. G. *Mysterium coniunctionis*.'
},
'13': {
    'cor': 'Prateado',
    'rgb': (192, 192, 192),
    'anima_animus': 'Intuição, reflexão, o feminino arquetípico (Lua), clareza mental sutil, modernidade, valor intrínseco.',
    'sombra': 'Frieza, distanciamento emocional, ilusão, indecisão, superficialidade elegante, inconstância.',
    'personalidade': 'Intuitiva, elegante, sofisticada, busca harmonia e paz interior, pode ser adaptável.',
    'diagnostico': 'Pode indicar necessidade de introspecção, conexão com a intuição e o feminino, ou um período de purificação e clareza.',
    'referencias': 'Conceitos: Anima, Simbolismo Lunar, Inconsciente, Intuição.'
},
'14': {
    'cor': 'Turquesa/Ciano',
    'rgb': (64, 224, 208),
    'anima_animus': 'Cura emocional, comunicação clara (especialmente do coração), proteção, individualidade, tranquilidade expressiva.',
    'sombra': 'Dificuldade em expressar sentimentos, isolamento autoimposto, frieza defensiva, superficialidade na comunicação.',
    'personalidade': 'Calma, comunicativa, criativa, independente, busca clareza e expressão autêntica, curativa.',
    'diagnostico': 'Pode indicar necessidade de cura emocional, melhoria na comunicação (falar a sua verdade), ou fortalecimento da individualidade e autoconfiança.',
    'referencias': 'Conceitos: Comunicação, Cura Emocional. Interseção simbólica de Azul e Verde.'
},
'15': {
    'cor': 'Magenta',
    'rgb': (255, 0, 255),
    'anima_animus': 'Espiritualidade prática, harmonia universal, compaixão não sentimental, transformação interior, gratidão.',
    'sombra': 'Excentricidade, não praticidade, sentimento de superioridade espiritual, desequilíbrio emocional.',
    'personalidade': 'Inovadora, artística, compassiva, busca equilíbrio entre o espiritual e o material, inconformista.',
    'diagnostico': 'Pode indicar um período de grande insight espiritual, necessidade de alinhar ações com valores elevados, ou de expressar compaixão de forma ativa.',
    'referencias': 'Conceitos: União dos Opostos (simbólica), Espiritualidade Integrada.'
},
'16': {
    'cor': 'Índigo',
    'rgb': (75, 0, 130),
    'anima_animus': 'Intuição profunda (terceiro olho), sabedoria interior, percepção além do comum, autoridade espiritual, integridade.',
    'sombra': 'Medo do desconhecido, fanatismo, isolamento por se sentir incompreendido, depressão por excesso de percepção, dogmatismo.',
    'personalidade': 'Introspectiva, sábia, perceptiva, busca conhecimento profundo e verdade, pode ser vista como "diferente".',
    'diagnostico': 'Pode indicar uma forte conexão com o inconsciente, necessidade de confiar na intuição, ou um período de busca por respostas existenciais e integridade.',
    'referencias': 'Conceitos: Função Intuição Introvertida, Sabedoria Interior. Obras relevantes: JUNG, C. G. *Tipos psicológicos*.'
},
'17': {
    'cor': 'Verde Oliva',
    'rgb': (128, 128, 0),
    'anima_animus': 'Paz, sabedoria prática, conexão com a natureza de forma madura, esperança resiliente, estratégia.',
    'sombra': 'Amargura, ressentimento, engano, estagnação disfarçada de paz, covardia.',
    'personalidade': 'Diplomática, observadora, perspicaz, valoriza a harmonia e a estratégia, resiliente.',
    'diagnostico': 'Pode indicar necessidade de resolução de conflitos (internos ou externos), busca por paz interior duradoura, ou aplicação da sabedoria de forma prática.',
    'referencias': 'Conceitos: Sabedoria Terrena, Paz. Interseção simbólica de Verde e Amarelo/Marrom.'
},
'18': {
    'cor': 'Verde Limão (Chartreuse)',
    'rgb': (127, 255, 0),
    'anima_animus': 'Juventude, vigor, otimismo efervescente, clareza mental e emocional, novidade, espontaneidade.',
    'sombra': 'Imaturidade, inveja aguda, acidez, irritabilidade, ansiedade por novidade.',
    'personalidade': 'Energética, alegre, comunicativa, pode ser um pouco impulsiva ou superficial, inovadora.',
    'diagnostico': 'Pode indicar necessidade de renovação, leveza, ou um alerta para não ser excessivamente crítico, invejoso ou ansioso por constante mudança.',
    'referencias': 'Conceitos: Energia Jovem, Novidade. Interseção simbólica de Verde e Amarelo.'
},
'19': {
    'cor': 'Azul Celeste/Claro',
    'rgb': (173, 216, 230),
    'anima_animus': 'Paz, tranquilidade, serenidade, comunicação suave, esperança e proteção espiritual, o céu.',
    'sombra': 'Passividade, ingenuidade, frieza distante, dificuldade em impor limites, tristeza suave.',
    'personalidade': 'Calma, sonhadora, idealista, busca harmonia e entendimento, gentil.',
    'diagnostico': 'Pode indicar necessidade de paz interior, relaxamento, ou desenvolvimento de uma comunicação mais assertiva e suave, ou um toque de melancolia.',
    'referencias': 'Conceitos: Tranquilidade, Espiritualidade Serena. Simbolismo do Céu.'
},
'20': {
    'cor': 'Azul Marinho',
    'rgb': (0, 0, buscar_cor_proxima(color_norm_rgb_item, cores_junguianas)
                    if cor_jung_especifica and cor_jung_especifica['cor'] != 'N/A':
                        with st.expander(f"Análise Junguiana: {cor_jung_especifica['cor']}", expanded=False):
                            st.write(f"**Anima/Animus:** {cor_jung_especifica['anima_animus']}")
                            st.write(f"**Sombra:** {cor_jung_especifica['sombra']}")
                            st.write(f"**Personalidade:** {cor_jung_especifica['personalidade']}")
                            st.write(f"**Diagnóstico:** {cor_jung_especifica['diagnostico']}")
                            if 'referencias' in cor_jung_especifica and cor_jung_especifica['referencias']:
                                st.markdown("**Pistas para Estudo:**"); st.caption(cor_jung_especifica['referencias'])
                    else: st.caption("(Análise Junguiana não disponível para esta cor)")
            st.markdown(f"---")

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
                    with col_camada_img: st.image(camada_imagem_rgb, use_container_width=True, caption=f"Áreas para pintar com a Cor {i+1} (RGB: {tuple(cor_atual_uint8_rgb)})")
                    camada_imagem_bgr = cv2.cvtColor(camada_imagem_rgb, cv2.COLOR_RGB2BGR)
                    _, camada_buffer = cv2.imencode('.png', camada_imagem_bgr)
                    with col_camada_info:
                        st.download_button(label=f"📥 Baixar Camada Cor {i+1}", data=camada_buffer.tobytes(), file_name=f'camada_cor_{i+1}_{uploaded_file.name}.png', mime='image/png', key=f"download_camada_{i}")
                        st.markdown("**Cor de Referência:**")
                        color_block_ref = np.full((50, 50, 3), cor_atual_uint8_rgb, dtype=np.uint8)
                        st.image(color_block_ref, width=50)
                    st.markdown("---") 
            else: st.info("Paleta de cores não disponível para gerar camadas.")

            # --- Geração de PDF Simplificado ---
            st.write("---")
            st.subheader("📄 Opções de Relatório")
            # Adicionado um id ao botão para poder escondê-lo na impressão via CSS
            st.markdown('<div id="generate-pdf-button">', unsafe_allow_html=True)
            if st.button("Gerar Relatório PDF Simplificado", key="generate_pdf_button_click", help="Gera um PDF com os principais resultados textuais e imagens."):
                with st.spinner("Gerando PDF..."):
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_auto_page_break(auto=True, margin=15)
                    
                    # Tentar adicionar fonte DejaVu para melhor suporte a Unicode
                    try:
                        # Certifique-se que 'DejaVuSansCondensed.ttf' está na mesma pasta do script
                        # ou forneça o caminho completo.
                        pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
                        pdf.set_font("DejaVu", size=12)
                    except RuntimeError:
                        st.warning("Fonte DejaVu (DejaVuSansCondensed.ttf) não encontrada. Usando Arial (pode haver problemas com caracteres especiais). Certifique-se de que o arquivo .ttf está na pasta do script.")
                        pdf.set_font("Arial", size=12)

                    pdf.set_font_size(16) # Usar set_font_size para mudar o tamanho
                    pdf.cell(0, 10, "Relatório de Análise de Imagem e Cores", 0, 1, "C")
                    pdf.ln(5)

                    pdf.set_font_size(12)
                    pdf.cell(0, 10, f"Arquivo Original: {uploaded_file.name}", 0, 1)
                    pdf.ln(5)
                    
                    # Função auxiliar para adicionar imagem ao PDF
                    def add_image_to_pdf(pdf_obj, image_pil_or_cv, title, temp_filename_base, is_cv_img=False):
                        pdf_obj.set_font_size(12) # Resetar tamanho da fonte para o título da imagem
                        pdf_obj.cell(0, 10, title, 0, 1)
                        try:
                            temp_path = f"{temp_filename_base}.png"
                            if is_cv_img: # Se for uma imagem OpenCV (NumPy array)
                                if len(image_pil_or_cv.shape) == 2: # Grayscale
                                    cv2.imwrite(temp_path, image_pil_or_cv)
                                    img_pil = Image.open(temp_path) # Reabre como PIL para pegar dimensões
                                else: # Color (RGB passado, converter para BGR para OpenCV)
                                    cv2.imwrite(temp_path, cv2.cvtColor(image_pil_or_cv, cv2.COLOR_RGB2BGR))
                                    img_pil = Image.open(temp_path)
                            else: # É uma imagem PIL
                                image_pil_or_cv.save(temp_path)
                                img_pil = image_pil_or_cv

                            img_w, img_h = img_pil.size
                            ratio = img_h / img_w if img_w > 0 else 1
                            display_w = min(180, pdf_obj.w - 2 * pdf_obj.l_margin) 
                            display_h = display_w * ratio
                            max_h = 70 
                            if display_h > max_h:
                                display_h = max_h
                                display_w = display_h / ratio if ratio > 0 else display_h
                            
                            current_x = pdf_obj.get_x()
                            current_y = pdf_obj.get_y()
                            if current_y + display_h > pdf_obj.page_break_trigger: 
                                pdf_obj.add_page()
                                current_y = pdf_obj.get_y() # Pega o novo Y após quebra de página

                            if display_w > 0 and display_h > 0:
                                pdf_obj.image(temp_path, x=current_x, y=current_y, w=display_w, h=display_h)
                                pdf_obj.ln(display_h + 5) 
                            else:
                                pdf_obj.cell(0,10, f"Dimensões inválidas para imagem '{title}'.",0,1)

                            os.remove(temp_path)
                        except Exception as e_img:
                            pdf_obj.set_font_size(10)
                            pdf_obj.multi_cell(0, 5, f"Erro ao adicionar imagem '{title}': {str(e_img)}", 0, 1)
                            pdf_obj.ln(5)

                    add_image_to_pdf(pdf, pil_image, "Imagem Original:", "temp_original_pdf")
                    add_image_to_pdf(pdf, segmented_image_uint8_rgb, "Imagem Segmentada:", "temp_segmented_pdf", is_cv_img=True)
                    add_image_to_pdf(pdf, result_paint_screen, "Tela para Pintar:", "temp_paint_screen_pdf", is_cv_img=True)

                    pdf.set_font_size(14); pdf.cell(0, 10, "Análise da Cor Representativa da Paleta", 0, 1); pdf.set_font_size(10)
                    if cor_jung_representativa and cor_jung_representativa['cor'] != 'N/A':
                        text_content = (
                            f"Cor: {cor_jung_representativa['cor']}\n"
                            f"Anima/Animus: {cor_jung_representativa['anima_animus']}\n"
                            f"Sombra: {cor_jung_representativa['sombra']}\n"
                            f"Personalidade: {cor_jung_representativa['personalidade']}\n"
                            f"Diagnóstico: {cor_jung_representativa['diagnostico']}\n"
                            f"Pistas para Estudo: {cor_jung_representativa.get('referencias', '')}"
                        )
                        pdf.multi_cell(0, 5, text_content)
                    pdf.ln(5)

                    pdf.set_font_size(14); pdf.cell(0, 10, "Detalhes das Cores da Paleta", 0, 1)
                    for i, color_norm_rgb_item in enumerate(colors_palette_norm_rgb):
                        pdf.set_font_size(11); pdf.cell(0, 7, f"Cor {i+1}", 0, 1); pdf.set_font_size(9) # Reduzido para caber mais
                        r_norm, g_norm, b_norm = color_norm_rgb_item[0], color_norm_rgb_item[1], color_norm_rgb_item[2]
                        c_ml, m_ml, y_ml, k_ml, white_ml = calculate_ml_with_white(r_norm, g_norm, b_norm, total_ml_slider)
                        
                        text_palette_detail = (
                            f"RGB: ({int(r_norm*255)}, {int(g_norm*255)}, {int(b_norm*255)})\n"
                            f"Dosagem para {total_ml_slider}ml (incl. Branco):\n"
                            f"  Ciano (C): {c_ml:.1f} ml, Magenta (M): {m_ml:.1f} ml, Amarelo (Y): {y_ml:.1f} ml, Preto (K): {k_ml:.1f} ml, Branco (W): {white_ml:.1f} ml"
                        )
                        pdf.multi_cell(0, 5, text_palette_detail)

                        cor_jung_especifica = buscar_cor_proxima(color_norm_rgb_item, cores_junguianas)
                        if cor_jung_especifica and cor_jung_especifica['cor'] != 'N/A':
                             text_jung_detail = (
                                 f"Análise Junguiana ({cor_jung_especifica['cor']}):\n"
                                 f"  Anima/Animus: {cor_jung_especifica['anima_animus']}\n"
                                 f"  Sombra: {cor_jung_especifica['sombra']}\n"
                                 f"  Personalidade: {cor_jung_especifica['personalidade']}\n" 
                                 f"  Diagnóstico: {cor_jung_especifica['diagnostico']}\n" 
                                 f"  Pistas para Estudo: {cor_jung_especifica.get('referencias', '')}"
                             )
                             pdf.multi_cell(0, 5, text_jung_detail)
                        pdf.ln(2)
                    
                    pdf.set_font_size(14); pdf.cell(0, 10, "Camadas de Cores para Pintura", 0, 1); pdf.set_font_size(10)
                    pdf.multi_cell(0,5, "As imagens das camadas individuais podem ser baixadas diretamente da interface web (não incluídas neste PDF para simplificação).")

                    pdf_data = pdf.output(dest='S').encode('latin-1') # 'S' para string, latin-1 para bytes
                    
                    st.download_button(label="📥 Baixar Relatório PDF Completo", data=pdf_data,
                                       file_name=f"relatorio_completo_{uploaded_file.name}.pdf",
                                       mime="application/pdf", key="download_pdf_report_button")
            st.markdown('</div>', unsafe_allow_html=True) # Fecha a div do botão de gerar PDF

    except UnidentifiedImageError:
        st.error("Erro ao abrir a imagem. O arquivo pode estar corrompido ou não é um formato de imagem suportado.")
    except Exception as e:
        st.error(f"Ocorreu um erro inesperado durante o processamento: {e}")
        st.error("Detalhes técnicos:")
        st.exception(e) 
else:
    st.warning("Por favor, carregue uma imagem para gerar a paleta e a tela.")
else:
if not uploaded_file :
st.info("👈 Ajuste as configurações na barra lateral, carregue uma imagem e clique em 'Gerar Paleta e Tela'.")

                    
