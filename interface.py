#pip install PyQt5
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QStackedWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt

class Interface(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simulador de Instruções")
        self.setGeometry(200, 200, 1100, 700)
        
        self.instrução_atual = None
        
        layout_inicial = QVBoxLayout(self)
        self.menu_stack = QStackedWidget()
        
        self.registrador_ax_input = QLineEdit("0000")
        self.registrador_bx_input = QLineEdit("0000")
        self.registrador_cx_input = QLineEdit("0000")
        self.registrador_dx_input = QLineEdit("0000")  
        
        self.registrador_cs_input = QLineEdit("4000")
        self.registrador_ss_input = QLineEdit("5000")
        self.registrador_ds_input = QLineEdit("6000")
        self.registrador_es_input = QLineEdit("7000")
        
        self.registrador_ip_input = QLineEdit("0100")  
        self.registrador_sp_input = QLineEdit("FFFF")  
        self.registrador_bp_input = QLineEdit("0000")  
        self.registrador_di_input = QLineEdit("0000")  
        self.registrador_si_input = QLineEdit("0000")  

        self.registrador_flag_input = QLineEdit()  
        
        self.memoria = bytearray(1048576)
        
        self.cor_borda_style = "background-color: #FFFFF0; border: 2px solid #FF0000; padding: 3px;"
        self.barramento_ativo_style = "background-color: #FFFFF0; border: 2px solid #FF0000; padding: 10px; font-weight: bold; font-size: 14px; color: black"
        self.barramento_inativo_style = "background-color: #EEEEEE; border: 1px dashed #999; padding: 10px; font-size: 14px; color: #777"
        
        self.demonstracao_estado = "Inicio"
        self.demonstracao_passo_interno = 0
        self.demonstracao_operacao = ""
        self.demonstracao_dst_str = ""
        self.demonstracao_src_str = ""
        self.demonstracao_imediato_str = ""
        self.demonstracao_dados_dst = 0
        self.demonstracao_dados_src = 0
        self.demonstracao_endereco_calculado = 0
        self.demonstracao_tempo_byte = 0
        self.demonstracao_ip_inicial = 0
        
        self.operacao_c = QComboBox()
        self.operacao_c.addItems(["MOV"])
        self.dst_c = QComboBox()
        self.dst_c.addItems(["AX", "BX", "CX", "DX", "[SI]", "[DI]"])
        self.src_c = QComboBox()
        self.src_c.addItems(["AX", "BX", "CX", "DX", "[SI]", "[DI]"])
        
        self.demonstracao_label_ax = QLabel("0000")
        self.demonstracao_label_bx = QLabel("0000")
        self.demonstracao_label_cx = QLabel("0000")
        self.demonstracao_label_dx = QLabel("0000")
        self.demonstracao_label_cs = QLabel("4000")
        self.demonstracao_label_ss = QLabel("5000")
        self.demonstracao_label_ds = QLabel("6000")
        self.demonstracao_label_es = QLabel("7000")
        self.demonstracao_label_ip = QLabel("0100")
        self.demonstracao_label_sp = QLabel("FFFF")
        self.demonstracao_label_bp = QLabel("0000")
        self.demonstracao_label_di = QLabel("0000")
        self.demonstracao_label_si = QLabel("0000")
        self.demonstracao_label_flag = QLabel("0000")

            
        self.label_demonstracao_intrucao = QLabel("Instrução: N/A")
        
        self.tela_barramento_endereco = QLabel("")
        self.tela_barramento_endereco.setAlignment(Qt.AlignCenter)
        self.tela_barramento_endereco.setWordWrap(True)
        self.tela_barramento_dados = QLabel("")
        self.tela_barramento_dados.setAlignment(Qt.AlignCenter)
        
        self.memoria_edicao_ef = QLineEdit("")
        self.memoria_edicao_ef.setPlaceholderText("Endereço Físico")
        self.memoria_edicao_valor = QLineEdit("")
        self.memoria_edicao_valor.setPlaceholderText("Valor do EF")
        
        self.log_memoria = QTextEdit()
        self.log_memoria.setReadOnly(True)
        self.log_memoria.setFontFamily("Courier")
        self.log_memoria.setStyleSheet("color: black;")
                
        pagina_inicial = self.menu_principal()
        pagina_moves = self.menu_moves()
        pagina_arithmetic = self.menu_arithmetic()
        pagina_boolean = self.menu_boolean()
        pagina_compare = self.menu_compare()
        pagina_jxx = self.menu_jxx()
        pagina_registrador = self.menu_registradores()
        pagina_demonstracao = self.menu_demonstracao()
        
        self.menu_stack.addWidget(pagina_inicial)
        self.menu_stack.addWidget(pagina_moves)
        self.menu_stack.addWidget(pagina_arithmetic)
        self.menu_stack.addWidget(pagina_boolean)
        self.menu_stack.addWidget(pagina_compare)
        self.menu_stack.addWidget(pagina_jxx)
        self.menu_stack.addWidget(pagina_registrador)
        self.menu_stack.addWidget(pagina_demonstracao)
        
        self.label_resultado = QLabel("Selecione uma instrução")
        self.label_resultado.setAlignment(Qt.AlignCenter)
        self.label_resultado.setStyleSheet("font-size: 14px; color: #333; padding: 10px;")
        
        linha = QFrame()
        linha.setFrameShape(QFrame.HLine)
        linha.setFrameShadow(QFrame.Sunken)
        linha.setStyleSheet("background-color: black; max-height: 2px;")  
        
        layout_inicial.addWidget(self.label_resultado, 0)
        layout_inicial.addWidget(linha, 0)
        layout_inicial.addWidget(self.menu_stack, 1)  
        
    def menu_principal(self):
        pagina = QWidget()
        layout = QVBoxLayout(pagina)
        layout_botoes = QHBoxLayout()
        
        btn_moves = QPushButton("Moves")
        btn_moves.clicked.connect(lambda: self.menu_stack.setCurrentIndex(1))
        layout_botoes.addWidget(btn_moves)
        
        btn_aritHmetic = QPushButton("Arithmetic")
        btn_aritHmetic.clicked.connect(lambda: self.menu_stack.setCurrentIndex(2))
        layout_botoes.addWidget(btn_aritHmetic)
        
        btn_boolean = QPushButton("Boolean")
        btn_boolean.clicked.connect(lambda: self.menu_stack.setCurrentIndex(3))
        layout_botoes.addWidget(btn_boolean)
        
        btn_compare = QPushButton("Test/Compare")
        btn_compare.clicked.connect(lambda: self.menu_stack.setCurrentIndex(4))
        layout_botoes.addWidget(btn_compare)
        
        layout.addLayout(layout_botoes)
        layout.addStretch(1)
        return pagina
    
    def menu_moves(self):
        pagina = QWidget()
        layout = QVBoxLayout(pagina)
        
        btn_mov = QPushButton(" MOV DST, SRC")
        btn_mov.clicked.connect(lambda: self.Registradores("Função MOV"))
        layout.addWidget(btn_mov)
        
        btn_push = QPushButton(" PUSH SRC")
        btn_push.clicked.connect(lambda: self.Registradores("Função PUSH"))
        layout.addWidget(btn_push)
        
        btn_pop = QPushButton(" POP DST")
        btn_pop.clicked.connect(lambda: self.Registradores("Função POP"))
        layout.addWidget(btn_pop)
        
        btn_xchg = QPushButton(" XCHG DST, SRC")
        btn_xchg.clicked.connect(lambda: self.Registradores("Função XCHG"))
        layout.addWidget(btn_xchg)
        
        btn_voltar = QPushButton(" Voltar ao Menu Principal")
        btn_voltar.clicked.connect(lambda: self.menu_stack.setCurrentIndex(0))
        layout.addWidget(btn_voltar, alignment=Qt.AlignLeft)

        layout.addStretch(1)
        return pagina
    
    def menu_arithmetic(self):
        pagina = QWidget()
        layout = QVBoxLayout(pagina)
        
        btn_add = QPushButton(" ADD DST, SRC")
        btn_add.clicked.connect(lambda: self.Registradores("Função ADD"))
        layout.addWidget(btn_add)
        
        btn_sub = QPushButton(" SUB DST, SRC")
        btn_sub.clicked.connect(lambda: self.Registradores("Função SUB"))
        layout.addWidget(btn_sub)
        
        btn_mul = QPushButton(" MUL SRC")
        btn_mul.clicked.connect(lambda: self.Registradores("Função MUL"))
        layout.addWidget(btn_mul)
        
        btn_inc = QPushButton(" INC DST")
        btn_inc.clicked.connect(lambda: self.Registradores("Função INC"))
        layout.addWidget(btn_inc)
        
        btn_dec = QPushButton(" DEC DST")
        btn_dec.clicked.connect(lambda: self.Registradores("Função DEC"))
        layout.addWidget(btn_dec)
        
        btn_neg = QPushButton(" NEG DST")
        btn_neg.clicked.connect(lambda: self.Registradores("Função NEG"))
        layout.addWidget(btn_neg)
        
        btn_div = QPushButton(" DIV SRC")
        btn_div.clicked.connect(lambda: self.Registradores("Função DIV"))
        layout.addWidget(btn_div)
        
        btn_voltar = QPushButton(" Voltar ao Menu Principal")
        btn_voltar.clicked.connect(lambda: self.menu_stack.setCurrentIndex(0))
        layout.addWidget(btn_voltar, alignment=Qt.AlignLeft)
        
        layout.addStretch(1)
        return pagina
    
    def menu_boolean(self):
        pagina = QWidget()
        layout = QVBoxLayout(pagina)
        
        
        btn_and = QPushButton(" AND DST, SRC")
        btn_and.clicked.connect(lambda: self.Registradores("Função AND"))
        layout.addWidget(btn_and)
        
        btn_or = QPushButton(" OR DST, SRC")
        btn_or.clicked.connect(lambda: self.Registradores("Função OR"))
        layout.addWidget(btn_or)
        
        btn_xor = QPushButton(" XOR DST, SRC")
        btn_xor.clicked.connect(lambda: self.Registradores("Função XOR"))
        layout.addWidget(btn_xor)
        
        btn_not = QPushButton(" NOT DST")
        btn_not.clicked.connect(lambda: self.Registradores("Função NOT"))
        layout.addWidget(btn_not)
        
        btn_voltar = QPushButton(" Voltar ao Menu Principal")
        btn_voltar.clicked.connect(lambda: self.menu_stack.setCurrentIndex(0))
        layout.addWidget(btn_voltar, alignment=Qt.AlignLeft)
        
        layout.addStretch(1)
        return pagina
    
    def menu_compare(self):
        pagina = QWidget()
        layout = QVBoxLayout(pagina)
        
        btn_cmp = QPushButton(" CMP SRC1, SRC2")
        btn_cmp.clicked.connect(lambda: self.Registradores("Função CMP"))
        layout.addWidget(btn_cmp)
        
        btn_jmp = QPushButton(" JMP ADDR")
        btn_jmp.clicked.connect(lambda: self.Registradores("Função JMP"))
        layout.addWidget(btn_jmp)
        
        btn_jxx = QPushButton(" Jxx ADDR")
        btn_jxx.clicked.connect(lambda: self.menu_stack.setCurrentIndex(5))
        layout.addWidget(btn_jxx)
        
        btn_call = QPushButton(" CALL ADDR")
        btn_call.clicked.connect(lambda: self.Registradores("Função CALL"))
        layout.addWidget(btn_call)
        
        btn_ret = QPushButton(" RET")
        btn_ret.clicked.connect(lambda: self.Registradores("Função RET"))
        layout.addWidget(btn_ret)
        
        btn_iret = QPushButton(" IRET")
        btn_iret.clicked.connect(lambda: self.Registradores("Função IRET"))
        layout.addWidget(btn_iret)
        
        btn_loop = QPushButton(" LOOP ADDR")
        btn_loop.clicked.connect(lambda: self.Registradores("Função LOPP"))
        layout.addWidget(btn_loop)
        
        btn_in = QPushButton(" IN AX, PORT")
        btn_in.clicked.connect(lambda: self.Registradores("Função IN"))
        layout.addWidget(btn_in)
        
        btn_out = QPushButton(" OUT PORT, AX")
        btn_out.clicked.connect(lambda: self.Registradores("Função OUT"))
        layout.addWidget(btn_out)
        
        btn_voltar = QPushButton(" Voltar ao Menu Principal")
        btn_voltar.clicked.connect(lambda: self.menu_stack.setCurrentIndex(0))
        layout.addWidget(btn_voltar, alignment=Qt.AlignLeft)
        
        layout.addStretch(1)
        return pagina
    
    def menu_jxx(self):
        pagina = QWidget()
        layout = QVBoxLayout(pagina)
        
        btn_je = QPushButton(" JE ADDR")
        btn_je.clicked.connect(lambda: self.Registradores("Função JE"))
        layout.addWidget(btn_je)
        
        btn_jne = QPushButton(" JNE ADDR")
        btn_jne.clicked.connect(lambda: self.Registradores("Função JNE"))
        layout.addWidget(btn_jne)
        
        btn_jg = QPushButton(" JG ADDR")
        btn_jg.clicked.connect(lambda: self.Registradores("Função JG"))
        layout.addWidget(btn_jg)
        
        btn_jge = QPushButton(" JGE ADDR")
        btn_jge.clicked.connect(lambda: self.Registradores("Função JGE"))
        layout.addWidget(btn_jge)
        
        btn_jl = QPushButton(" JL ADDR")
        btn_jl.clicked.connect(lambda: self.Registradores("Função JL"))
        layout.addWidget(btn_jl)
        
        btn_jle = QPushButton(" JLE ADDR")
        btn_jle.clicked.connect(lambda: self.Registradores("Função JlE"))
        layout.addWidget(btn_jle)
        
        btn_voltar = QPushButton(" Voltar ao Menu Principal")
        btn_voltar.clicked.connect(lambda: self.menu_stack.setCurrentIndex(0))
        layout.addWidget(btn_voltar, alignment=Qt.AlignLeft)
        
        layout.addStretch(1)
        return pagina
    
    def menu_registradores(self):
        pagina = QWidget()
        layout_2 = QVBoxLayout(pagina)
        layout_2_esquerda = QVBoxLayout()
        layout_2_direita = QVBoxLayout()
        layout_2_configuracao = QHBoxLayout()
        layout_2.setSpacing(10)
        
        Box_Style = "QGroupBox { border: 1px solid black; border-radius: 5px; margin-top: 1ex;}" "QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top left; padding: 0 3px;}"
        
        Box_Geral = QGroupBox("Registrador Geral")
        Box_Geral.setStyleSheet(Box_Style)
        Geral = QGridLayout()
        Geral.addWidget(QLabel("AX:"), 0,0); Geral.addWidget(self.registrador_ax_input, 0,1)
        Geral.addWidget(QLabel("BX:"), 0,2); Geral.addWidget(self.registrador_bx_input, 0,3)
        Geral.addWidget(QLabel("CX:"), 1,0); Geral.addWidget(self.registrador_cx_input, 1,1)
        Geral.addWidget(QLabel("DX:"), 1,2); Geral.addWidget(self.registrador_dx_input, 1,3)
        Box_Geral.setLayout(Geral); layout_2_esquerda.addWidget(Box_Geral)
        
        Box_Segmentos = QGroupBox("Registrador de Segmentos")
        Box_Segmentos.setStyleSheet(Box_Style)
        Segmentos = QGridLayout()
        Segmentos.addWidget(QLabel("CS:"), 0,0); Segmentos.addWidget(self.registrador_cs_input, 0,1) 
        Segmentos.addWidget(QLabel("SS:"), 0,2); Segmentos.addWidget(self.registrador_ss_input, 0,3)
        Segmentos.addWidget(QLabel("DS:"), 1,0); Segmentos.addWidget(self.registrador_ds_input, 1,1)
        Segmentos.addWidget(QLabel("ES:"), 1,2); Segmentos.addWidget(self.registrador_es_input, 1,3)
        Box_Segmentos.setLayout(Segmentos); layout_2_esquerda.addWidget(Box_Segmentos)
        
        Box_Offsets = QGroupBox("Registrador de Offsets")
        Box_Offsets.setStyleSheet(Box_Style)
        Offsets = QGridLayout()
        Offsets.addWidget(QLabel("IP:"), 0,0); Offsets.addWidget(self.registrador_ip_input, 0,1)
        Offsets.addWidget(QLabel("SP:"), 0,2); Offsets.addWidget(self.registrador_sp_input, 0,3)
        Offsets.addWidget(QLabel("BP:"), 1,0); Offsets.addWidget(self.registrador_bp_input, 1,1)
        Offsets.addWidget(QLabel("DI:"), 1,2); Offsets.addWidget(self.registrador_di_input, 1,3)
        Offsets.addWidget(QLabel("SI:"), 2,0); Offsets.addWidget(self.registrador_si_input, 2,1)
        Box_Offsets.setLayout(Offsets); layout_2_esquerda.addWidget(Box_Offsets)
        
        Box_Flag = QGroupBox("Registrador de Flags")
        Box_Flag.setStyleSheet(Box_Style)
        Flag = QGridLayout()
        Flag.addWidget(QLabel("FLAGS:"), 0,0); Flag.addWidget(self.registrador_flag_input, 0,1)
        Box_Flag.setLayout(Flag); layout_2_esquerda.addWidget(Box_Flag)
        
        layout_2_esquerda.addStretch(1)
        layout_2_configuracao.addLayout(layout_2_esquerda)
        
        Box_Instrução = QGroupBox("Instrução Atual")
        Box_Instrução.setStyleSheet(Box_Style)
        Instrucao = QGridLayout()
        Instrucao.addWidget(QLabel("Operação:"), 0,0); Instrucao.addWidget(self.operacao_c, 0,1)
        Instrucao.addWidget(QLabel("Destino (DST):"), 1,0); Instrucao.addWidget(self.dst_c, 1,1)
        Instrucao.addWidget(QLabel("Origem (SRC):"), 2,0); Instrucao.addWidget(self.src_c, 2,1)
        Box_Instrução.setLayout(Instrucao); layout_2_direita.addWidget(Box_Instrução)
        
        layout_2_direita.addStretch(1)
        layout_2_configuracao.addLayout(layout_2_direita)
        
        layout_2.addLayout(layout_2_configuracao)
        
        btn_demonstrar = QPushButton(" Demonstrar a execução da Instrução")
        btn_demonstrar.setStyleSheet("font-size: 14px; background-color: #DDEEFF; padding: 8px;")
        btn_demonstrar.clicked.connect(self.iniciar_demonstracao)
        layout_2.addWidget(btn_demonstrar)
        
        btn_voltar = QPushButton(" Voltar ao Menu Principal")
        btn_voltar.clicked.connect(lambda: self.menu_stack.setCurrentIndex(0))
        layout_2.addWidget(btn_voltar, alignment=Qt.AlignLeft)
        
        return pagina
    
    def menu_demonstracao(self):
        pagina = QWidget()
        layout = QHBoxLayout(pagina)
        
        parte_cpu = QVBoxLayout()
        Box_Style = "QGroupBox { border: 1px solid black; border-radius: 5px; margin-top: 1ex;}" "QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top left; padding: 0 3px;}"

        self.label_demonstracao_intrucao.setStyleSheet("font-size: 16px; font-weight: bold; color: #000080; padding: 5px;")
        self.label_demonstracao_intrucao.setAlignment(Qt.AlignCenter)
        parte_cpu.addWidget(self.label_demonstracao_intrucao)
        
        Box_Geral = QGroupBox("Registrador Geral")
        Box_Geral.setStyleSheet(Box_Style)
        Geral = QGridLayout()
        Geral.addWidget(QLabel("AX:"), 0,0); Geral.addWidget(self.demonstracao_label_ax, 0,1)
        Geral.addWidget(QLabel("BX:"), 0,2); Geral.addWidget(self.demonstracao_label_bx, 0,3)
        Geral.addWidget(QLabel("CX:"), 1,0); Geral.addWidget(self.demonstracao_label_cx, 1,1)
        Geral.addWidget(QLabel("DX:"), 1,2); Geral.addWidget(self.demonstracao_label_dx, 1,3)
        Box_Geral.setLayout(Geral); parte_cpu.addWidget(Box_Geral)
        
        Box_Segmentos = QGroupBox("Registrador de Segmentos")
        Box_Segmentos.setStyleSheet(Box_Style)
        Segmentos = QGridLayout()
        Segmentos.addWidget(QLabel("CS:"), 0,0); Segmentos.addWidget(self.demonstracao_label_cs, 0,1) 
        Segmentos.addWidget(QLabel("SS:"), 0,2); Segmentos.addWidget(self.demonstracao_label_ss, 0,3)
        Segmentos.addWidget(QLabel("DS:"), 1,0); Segmentos.addWidget(self.demonstracao_label_ds, 1,1)
        Segmentos.addWidget(QLabel("ES:"), 1,2); Segmentos.addWidget(self.demonstracao_label_es, 1,3)
        Box_Segmentos.setLayout(Segmentos); parte_cpu.addWidget(Box_Segmentos)
        
        Box_Offsets = QGroupBox("Registrador de Offsets")
        Box_Offsets.setStyleSheet(Box_Style)
        Offsets = QGridLayout()
        Offsets.addWidget(QLabel("IP:"), 0,0); Offsets.addWidget(self.demonstracao_label_ip, 0,1)
        Offsets.addWidget(QLabel("SP:"), 0,2); Offsets.addWidget(self.demonstracao_label_sp, 0,3)
        Offsets.addWidget(QLabel("BP:"), 1,0); Offsets.addWidget(self.demonstracao_label_bp, 1,1)
        Offsets.addWidget(QLabel("DI:"), 1,2); Offsets.addWidget(self.demonstracao_label_di, 1,3)
        Offsets.addWidget(QLabel("SI:"), 2,0); Offsets.addWidget(self.demonstracao_label_si, 2,1)
        Box_Offsets.setLayout(Offsets); parte_cpu.addWidget(Box_Offsets)
        
        Box_Flag = QGroupBox("Registrador de Flags")
        Box_Flag.setStyleSheet(Box_Style)
        Flag = QGridLayout()
        Flag.addWidget(QLabel("FLAGS:"), 0,0); Flag.addWidget(self.demonstracao_label_flag, 0,1)
        Box_Flag.setLayout(Flag); parte_cpu.addWidget(Box_Flag)
        
        parte_cpu.addStretch(1)
        layout.addLayout(parte_cpu, 1)
        
        parte_central = QVBoxLayout()
        parte_central.setSpacing(20)
        
        Box_Barramento = QGroupBox("Fluxo de Barramento")
        Box_Barramento.setStyleSheet(Box_Style)
        layout_barramento = QVBoxLayout()
        layout_barramento.setSpacing(15)
        
        label_EF = QLabel("Barramento de Endereço (CPU ➡️ MEM)")
        label_EF.setStyleSheet("font-weight: bold; color: black;")
        self.tela_barramento_endereco.setStyleSheet(self.barramento_inativo_style)
        layout_barramento.addWidget(label_EF)
        layout_barramento.addWidget(self.tela_barramento_endereco)
        
        Seta = QLabel("⬇️ ⬆️")
        Seta.setAlignment(Qt.AlignCenter)
        Seta.setStyleSheet("font-size: 20px; font-weight: bold; color: black;")
        layout_barramento.addWidget(Seta)
        
        label_dado = QLabel("Barramento de Dados (CPU ⬅️ MEM)")
        label_dado.setStyleSheet("font-weight: bold; color: black;")
        self.tela_barramento_dados.setStyleSheet(self.barramento_inativo_style)
        layout_barramento.addWidget(label_dado)
        layout_barramento.addWidget(self.tela_barramento_dados)
        
        Box_Barramento.setLayout(layout_barramento)
        parte_central.addWidget(Box_Barramento)
        parte_central.addStretch(1)
        
        btn_proximo = QPushButton("Próximo Passo ➡️")
        btn_proximo.setStyleSheet("color: black")
        btn_proximo.clicked.connect(self.executar_passo_demonstracao)
        parte_central.addWidget(btn_proximo)
        
        btn_voltar = QPushButton("Voltar para a configuração")
        btn_voltar.clicked.connect(lambda: self.menu_stack.setCurrentIndex(6))
        parte_central.addWidget(btn_voltar)
        
        layout.addLayout(parte_central, 1)
        
        parte_memoria = QVBoxLayout()
        
        Box_Editor_Memoria = QGroupBox("Editor de Memória")
        Box_Editor_Memoria.setStyleSheet(Box_Style)
        layout_edicao = QGridLayout()
        layout_edicao.addWidget(QLabel("Endereço Físico:"), 0, 0)
        layout_edicao.addWidget(self.memoria_edicao_ef, 0, 1)
        layout_edicao.addWidget(QLabel("Valor:"), 1, 0)
        layout_edicao.addWidget(self.memoria_edicao_valor, 1, 1)
        
        btn_salvar_memoria = QPushButton("Salvar na Memória")
        btn_salvar_memoria.clicked.connect(self.salvar_memoria)
        layout_edicao.addWidget(btn_salvar_memoria, 2, 0, 1, 2)
        
        Box_Editor_Memoria.setLayout(layout_edicao)
        parte_memoria.addWidget(Box_Editor_Memoria)
        
        Box_Memoria_Log = QGroupBox("Memoria")
        Box_Memoria_Log.setStyleSheet(Box_Style)
        layout_log = QVBoxLayout()
        layout_log.addWidget(self.log_memoria)
        Box_Memoria_Log.setLayout(layout_log)
        parte_memoria.addWidget(Box_Memoria_Log)
        
        layout.addLayout(parte_memoria, 1)
        
        return pagina
        
    def salvar_memoria(self, text):
        try:
            ef_str = self.memoria_edicao_ef.text()
            valor_str = self.memoria_edicao_valor.text()
            
            if not ef_str or not valor_str:
                raise ValueError("Endereço físico e valor não podem estar vazios.")
            
            endereco_fisico = int(ef_str, 16)
            valor = int(valor_str, 16)
            
            info = ""
            if valor <= 0xFF:
                self.memoria[endereco_fisico] = valor
                info = f"Salvar: {valor:02X} em {endereco_fisico:X})"
            elif valor <= 0xFFFF:
                byte_baixo = valor & 0xFF
                byte_alto = (valor >> 8) & 0xFF
                self.memoria[endereco_fisico] = byte_baixo
                self.memoria[endereco_fisico + 1] = byte_alto
                info = f"Salvar: {valor:04X} em {endereco_fisico:X} )"
            else:
                raise ValueError("Valor excede 16 bits (FFFF)")
            
            self.log_memoria.setStyleSheet(self.cor_borda_style)
            self.log_memoria.append(info)
            
            QMessageBox.information(self, "Memória", "Valor salvo com sucesso na memória.")
        
        except ValueError as e:
            QMessageBox.warning(self, "Erro no Formato", f"Erro: {e}\n Use valores hexadecimais")
        except IndexError:
            QMessageBox.warning(self, "Erro de Endereço", f"Erro: Endereço 0x{endereco_fisico:X} esta fora do limite da memória.")
        except Exception as e:
            QMessageBox.critical(self, "Erro Inesperado", str(e))
    
    def iniciar_demonstracao(self):
        self.demonstracao_estado = "Busca_Opcode"
        self.demonstracao_passo_interno = 0
        self.demonstracao_tempo_byte = 0
        self.resetar_demonstracao()
        self.log_memoria.clear()
        
        self.demonstracao_ip_inicial = int(self.registrador_ip_input.text(), 16)
        
        self.demonstracao_label_ax.setText(self.registrador_ax_input.text())
        self.demonstracao_label_bx.setText(self.registrador_bx_input.text())
        self.demonstracao_label_cx.setText(self.registrador_cx_input.text())
        self.demonstracao_label_dx.setText(self.registrador_dx_input.text())
        self.demonstracao_label_cs.setText(self.registrador_cs_input.text())
        self.demonstracao_label_ss.setText(self.registrador_ss_input.text())
        self.demonstracao_label_ds.setText(self.registrador_ds_input.text())
        self.demonstracao_label_es.setText(self.registrador_es_input.text())
        self.demonstracao_label_ip.setText(self.registrador_ip_input.text())
        self.demonstracao_label_sp.setText(self.registrador_sp_input.text())
        self.demonstracao_label_bp.setText(self.registrador_bp_input.text())
        self.demonstracao_label_di.setText(self.registrador_di_input.text())
        self.demonstracao_label_si.setText(self.registrador_si_input.text())
        self.demonstracao_label_flag.setText(self.registrador_flag_input.text())

        self.demonstracao_operacao = self.operacao_c.currentText()
        self.demonstracao_dst_str = self.dst_c.currentText()
        self.demonstracao_src_str = self.src_c.currentText()
        
        instrucao_formatada = f"{self.demonstracao_operacao}, {self.demonstracao_dst_str}, {self.demonstracao_src_str}"
        self.label_demonstracao_intrucao.setText(f"Instrução: {instrucao_formatada}")
        
        self.menu_stack.setCurrentIndex(7)
        self.label_resultado.setText(f"Demonstrando: {instrucao_formatada}")
        
        EF_opcode = 0
        try:
            segmento_cs = int(self.demonstracao_label_cs.text(), 16)
            offset_ip = int(self.demonstracao_label_ip.text(), 16)
            EF_opcode = (segmento_cs * 16) + offset_ip
            
            self.memoria[EF_opcode] = 1
            self.memoria[EF_opcode + 1] = 2
            self.memoria[EF_opcode + 2] = 3
            
        except ValueError:
            pass
        except IndexError:
            QMessageBox.warning(self, "Erro de endereço"), f"Erro: Endereço CS:IP ({EF_opcode:X}) está fora da memória."
            self.menu_stack.setCurrentIndex(6)
            
    def executar_passo_demonstracao(self):
        self.resetar_demonstracao()
        self.log_memoria.setStyleSheet("")
        
        try:
            if self.demonstracao_estado == "Busca_Opcode":
                terminou = self.Passo_Busca(self.demonstracao_operacao, self.demonstracao_operacao, "Busca_DST")
                if terminou:
                    self.demonstracao_estado = "Busca_DST"
                    self.demonstracao_passo_interno = 0
                
            elif self.demonstracao_estado == "Busca_DST":
                terminou = self.Passo_Busca(self.demonstracao_dst_str, self.demonstracao_dst_str, "Busca_SRC")
                if terminou:
                    self.demonstracao_estado = "Busca_SRC"
                    self.demonstracao_passo_interno = 0
                    
            elif self.demonstracao_estado == "Busca_SRC":
                terminou = self.Passo_Busca(self.demonstracao_src_str, self.demonstracao_src_str, "Decodificação")
                if terminou:
                    self.demonstracao_estado = "Decodificacao"
                    self.demonstracao_passo_interno = 0
                    
            elif self.demonstracao_estado == "Decodificacao":
                if self.Passo_Decodificacao():
                    if self.demonstracao_src_str.startswith("["):
                        self.demonstracao_estado = "Busca_Operando_SRC"
                    elif self.demonstracao_dst_str.startswith("["):
                        self.demonstracao_estado = "Execucao"
                    else:
                        self.demonstracao_estado = "Execucao"
                        self.demonstracao_passo_interno = 0
            
            elif self.demonstracao_estado == "Busca_Operando_SRC":
                terminou_leitura = self.Passo_Leitura()
                if terminou_leitura:
                    self.demonstracao_estado = "Execucao"
                    self.demonstracao_passo_interno = 0
                    
            elif self.demonstracao_estado == "Execucao":
                if self.executar_passo_execucao():
                    if self.demonstracao_dst_str.startswith("["):
                        self.demonstracao_estado = "Escreve_Operando_DST"
                else:
                    self.demonstracao_estado = "Fim"
                self.demonstracao_passo_interno = 0
            
            elif self.demonstracao_estado == "Escreve_Operando_DST":
                if self.Passo_Escrita():  
                    self.demonstracao_estado = "Fim"
                    self.demonstracao_passo_interno = 0
            
            elif self.demonstracao_estado == "Fim":  
                self.tela_barramento_endereco.setText("Instrução Concluída.")
                self.tela_barramento_endereco.setStyleSheet(self.barramento_inativo_style)
                self.tela_barramento_dados.setText("Pronto para a próxima instrução.")
                self.tela_barramento_dados.setStyleSheet(self.barramento_inativo_style)
                
                ip_str_inicial = f"{self.demonstracao_ip_inicial:04X}"
                self.demonstracao_label_ip.setText(ip_str_inicial)
                self.registrador_ip_input.setText(ip_str_inicial)
                
                self.demonstracao_estado = "Busca_Opcode"
                self.demonstracao_passo_interno = 0
                
        except Exception as e:
            self.tela_barramento_endereco.setText(f"Erro: {e}")
            self.tela_barramento_endereco.setStyleSheet(self.barramento_ativo_style)
            self.demonstracao_estado = "Fim"
    
    def acesso_memoria(self, tipo, endereço, dado, comentario=""):
        if tipo =="Leitura":
            direcao_dado = "⬅️"
        else:
            direcao_dado ="➡️"
        
        dado_formatado = ""
        
        if comentario.startswith("(") and "Byte" not in comentario and "Valor" not in comentario:
            dado_formatado = comentario.strip("()")
        else:
            dado_formatado = f"{dado} {comentario}"
        
        linha_endereco = f"Endereço ➡️ {endereço}"
        linha_dado = f"Dado {direcao_dado} {dado_formatado}"
        
        self.log_memoria.append(linha_endereco)
        self.log_memoria.append(linha_dado)
        self.log_memoria.setStyleSheet(self.cor_borda_style)
    
    def Passo_Busca(self, nome_passo, dado_esperado, proximo_estado):
        if self.demonstracao_passo_interno ==0:
            self.demonstracao_label_cs.setStyleSheet(self.cor_borda_style)
            self.demonstracao_label_ip.setStyleSheet(self.cor_borda_style)
            self.tela_barramento_endereco.setText(f"Ciclo de busca: Identificando CS e IP (para {nome_passo})")
            self.tela_barramento_endereco.setStyleSheet(self.barramento_ativo_style)
            self.tela_barramento_dados.setStyleSheet(self.barramento_inativo_style)
            self.demonstracao_passo_interno = 1
            return False
        
        elif self.demonstracao_passo_interno ==1:
            segmento = int(self.demonstracao_label_cs.text(), 16)
            offset = int(self.demonstracao_label_ip.text(), 16)
            self.demonstracao_endereco_calculado = (segmento * 16) + offset
            calculo_str = f"Cálculo: (CS * 16) + IP\n(0x{segmento:X} * 16) + 0x{offset:X} = 0x{self.demonstracao_endereco_calculado:X}"
            self.tela_barramento_endereco.setText(f"➡️ {calculo_str}")
            self.tela_barramento_endereco.setStyleSheet(self.barramento_ativo_style)
            self.tela_barramento_dados.setStyleSheet(self.barramento_inativo_style)
            
            self.demonstracao_passo_interno = 2
            return False
        
        elif self.demonstracao_passo_interno == 2:
            dado = self.memoria[self.demonstracao_endereco_calculado]
            dado_str = f"{dado:02X}"
            self.tela_barramento_endereco.setStyleSheet(self.barramento_inativo_style)
            self.tela_barramento_dados.setText(f"⬅️ Memória retorna: {dado_esperado} ")
            self.tela_barramento_dados.setStyleSheet(self.barramento_ativo_style)
            
            self.acesso_memoria("Leitura", f"{self.demonstracao_endereco_calculado:X}", dado_esperado, f"({nome_passo})")
            self.demonstracao_passo_interno = 3
            
            return False
            
        elif self.demonstracao_passo_interno == 3:
            self.demonstracao_label_ip.setStyleSheet(self.cor_borda_style)
            offset_atual = int(self.demonstracao_label_ip.text(), 16)
            offset_novo = offset_atual + 2
            self.demonstracao_label_ip.setText(f"{offset_novo:04X}")
            self.tela_barramento_endereco.setText("CPU (Interno): Incrementa IP")
            self.tela_barramento_endereco.setStyleSheet(self.barramento_ativo_style)
            self.tela_barramento_dados.setStyleSheet(self.barramento_inativo_style)
            self.demonstracao_passo_interno = 0
            return True
        return False
    
    def Passo_Decodificacao(self):
        if self.demonstracao_passo_interno == 0:
            self.tela_barramento_endereco.setText(f"CPU (Interno): Decodificando\n{self.demonstracao_operacao} {self.demonstracao_dst_str}, {self.demonstracao_src_str}")
            self.tela_barramento_endereco.setStyleSheet(self.barramento_ativo_style)
            self.tela_barramento_dados.setStyleSheet(self.barramento_inativo_style)
            self.demonstracao_passo_interno = 1
            return False
        elif self.demonstracao_passo_interno == 1:
            if self.demonstracao_src_str in ["AX", "BX", "CX", "DX"]:
                self.demonstracao_dados_src = int(self.pegar_demonstracao_label(self.demonstracao_src_str).text(), 16)
        
            if self.demonstracao_dst_str in ["AX", "BX", "CX", "DX"]:
                self.demonstracao_dados_dst = int(self.pegar_demonstracao_label(self.demonstracao_dst_str).text(), 16)
            return True
            
    def Passo_Leitura(self):       
        registrador_offset_label = self.pegar_demonstracao_label(self.demonstracao_src_str.strip("[]"))
        registrador_offset_nome = self.demonstracao_src_str.strip("[]")
        
        if self.demonstracao_passo_interno == 0:
            self.demonstracao_label_ds.setStyleSheet(self.cor_borda_style)
            registrador_offset_nome.setStyleSheet(self.cor_borda_style)
            self.tela_barramento_endereco.setText(f"Leitura de Dados (SRC): Identificando DS e {registrador_offset_label} (p/ Byte Baixo)")
            self.tela_barramento_endereco.setStyleSheet(self.barramento_ativo_style)
            self.tela_barramento_dados.setStyleSheet(self.barramento_inativo_style)
            self.demonstracao_passo_interno = 1
            return False
        
        elif self.demonstracao_passo_interno == 1:
            segmento = int(self.demonstracao_label_ds.text(), 16)
            offset = int(registrador_offset_label.text(), 16)
            self.demonstracao_endereco_calculado = (segmento * 16) + offset
            calculo_str = f"Cálculo (SRC): (DS * 16) + {registrador_offset_nome}\n({segmento:X} * 16) + {offset:X} = 0x{self.demonstracao_endereco_calculado:X}"
            self.tela_barramento_endereco.setText(f"➡️ {calculo_str}")
            self.tela_barramento_endereco.setStyleSheet(self.barramento_ativo_style)
            self.tela_barramento_dados.setStyleSheet(self.barramento_inativo_style)
            
            byte_baixo = self.memoria[self.demonstracao_endereco_calculado]
            byte_alto = self.memoria[self.demonstracao_endereco_calculado + 1]
            
            if byte_baixo == 0x00 and byte_alto == 0x00:
                self.tela_barramento_dados.setText("Dado vazio. Aguardando no editor...")
                self.tela_barramento_dados.setStyleSheet(self.cor_borda_style)
                
                self.memoria_edicao_ef.setText(f"{self.demonstracao_endereco_calculado:X}")
                self.memoria_edicao_ef.setStyleSheet(self.cor_borda_style)
                self.memoria_edicao_valor.setText("")
                self.memoria_edicao_valor.setPlaceholderText("Digite o valor")
                self.memoria_edicao_valor.setStyleSheet(self.cor_borda_style)
                self.memoria_edicao_valor.setFocus()
                return False
                
            self.demonstracao_passo_interno = 2
            return False
        
        elif self.demonstracao_passo_interno == 2:
            byte_baixo = self.memoria[self.demonstracao_endereco_calculado]
            self.demonstracao_tempo_byte = byte_baixo
            dado_str = f"{byte_baixo:02X}"
            self.tela_barramento_endereco.setStyleSheet(self.barramento_inativo_style) 
            self.tela_barramento_dados.setText(f"⬅️ Memória retorna o Byte baixo: 0x{dado_str}")
            self.tela_barramento_dados.setStyleSheet(self.barramento_ativo_style)
            self.demonstracao_passo_interno = 3
            return False
            
        if self.demonstracao_passo_interno == 3:
            self.demonstracao_label_ds.setStyleSheet(self.cor_borda_style)     
            registrador_offset_label.setStyleSheet(self.cor_borda_style)
            self.tela_barramento_endereco.setText(f"Leitura (SRC): Identificando DS e {registrador_offset_nome}+1 (p/ Byte Alto)")
            self.tela_barramento_endereco.setStyleSheet(self.barramento_ativo_style)
            self.tela_barramento_dados.setStyleSheet(self.barramento_inativo_style)
            self.demonstracao_passo_interno = 4
            return False
        
        elif self.demonstracao_passo_interno == 4:
            segmento = int(self.demonstracao_label_ds.text(), 16)
            offset = int(registrador_offset_label.text(), 16) + 1
            self.demonstracao_endereco_calculado = (segmento * 16) + offset
            calculo_str = f"Cálculo (SRC): (DS * 16) + {registrador_offset_nome}+1\n(0x{segmento:X} * 16) + 0x{offset:X} = 0x{self.demonstracao_endereco_calculado:X}"
            self.tela_barramento_endereco.setText(f"➡️ {calculo_str}")
            self.tela_barramento_endereco.setStyleSheet(self.barramento_ativo_style)  
            self.tela_barramento_dados.setStyleSheet(self.barramento_inativo_style)
            self.demonstracao_passo_interno = 5
            return False
        
        elif self.demonstracao_passo_interno == 5:
            byte_alto = self.memoria[self.demonstracao_endereco_calculado]
            dado_str = f"{byte_alto:02X}"
            self.tela_barramento_endereco.setStyleSheet(self.barramento_inativo_style)
            self.tela_barramento_dados.setText(f"⬅️ Memória retorna o Byte alto: 0x{dado_str}")
            self.tela_barramento_dados.setStyleSheet(self.barramento_ativo_style)            
            self.demonstracao_dados_src = (byte_alto << 8) | self.demonstracao_tempo_byte
            self.demonstracao_passo_interno = 6
            return False
            
        elif self.demonstracao_passo_interno == 6:
            self.tela_barramento_endereco.setText(f"CPU (Interno): Montando valor 16 bits\nValor: 0x{self.demonstracao_dados_src:04X}")
            self.tela_barramento_endereco.setStyleSheet(self.barramento_ativo_style)
            self.tela_barramento_dados.setStyleSheet(self.barramento_inativo_style)
            
            endereço_alto = self.demonstracao_endereco_calculado
            endereço_baixo = endereço_alto - 1
            dado_completo_str = f"{self.demonstracao_dados_src:04X}"
            
            self.acesso_memoria("Leitura", f"{endereço_baixo:X}", dado_completo_str, "(Valor 16-bits)")            
            self.demonstracao_passo_interno = 0
            return True
        return False
        
    def executar_passo_execucao(self):   
        registrador_dst_label = self.pegar_demonstracao_label(self.demonstracao_dst_str)
        if self.demonstracao_passo_interno == 0:
            operacao = self.demonstracao_operacao
            dado_str = f"{self.demonstracao_dados_src:04X}"
            if operacao == "MOV":
                self.tela_barramento_endereco.setText(f"Execução: Movendo {dado_str} para {self.demonstracao_dst_str}")
                self.tela_barramento_endereco.setStyleSheet(self.barramento_ativo_style)
                self.tela_barramento_dados.setStyleSheet(self.barramento_inativo_style)
                registrador_dst_label.setText(dado_str)
                
                if self.demonstracao_dst_str == "AX":
                    self.registrador_ax_input.setText(dado_str)
                elif self.demonstracao_dst_str == "BX":
                    self.registrador_bx_input.setText(dado_str)
                elif self.demonstracao_dst_str == "CX":
                    self.registrador_cx_input.setText(dado_str)
                elif self.demonstracao_dst_str == "DX":
                    self.registrador_dx_input.setText(dado_str)
            
            registrador_dst_label.setStyleSheet(self.cor_borda_style)
            self.demonstracao_passo_interno = 1
            return False
        elif self.demonstracao_passo_interno == 1:
            return True
            
    def Passo_Escrita(self):
        registrador_offset_label = self.pegar_demonstracao_label(self.demonstracao_dst_str.strip("[]"))
        registrador_offset_nome = self.demonstracao_dst_str.strip("[]")
        self.demonstracao_dados_dst = self.demonstracao_dados_src
        byte_baixo = self.demonstracao_dados_dst & 0xFF
        byte_alto = (self.demonstracao_dados_dst >> 8) & 0xFF
        
        if self.demonstracao_passo_interno == 0:
            self.demonstracao_label_ds.setStyleSheet(self.cor_borda_style)
            registrador_offset_label.setStyleSheet(self.cor_borda_style)
            self.tela_barramento_endereco.setText(f"Escrita (DST): Identificando DS e {registrador_offset_nome} (p/ Byte Baixo)")
            self.tela_barramento_endereco.setStyleSheet(self.barramento_ativo_style)
            self.tela_barramento_dados.setStyleSheet(self.barramento_inativo_style)
            self.demonstracao_passo_interno = 1
            return False
        elif self.demonstracao_passo_interno == 1:
            segmento = int(self.demonstracao_label_ds.text(), 16)
            offset = int(registrador_offset_label.text(), 16)
            self.demonstracao_endereco_calculado = (segmento * 16) + offset
            calculo_str = f"Cálculo (DST): (DS * 16) + {registrador_offset_nome}\n(0x{segmento:X} * 16) + 0x{offset:X} = 0x{self.demonstracao_endereco_calculado:X}"
            self.tela_barramento_endereco.setText(f"➡️ {calculo_str}")
            self.tela_barramento_endereco.setStyleSheet(self.barramento_ativo_style)
            self.tela_barramento_dados.setStyleSheet(self.barramento_inativo_style)
            self.demonstracao_passo_interno = 2
            return False
        elif self.demonstracao_passo_interno == 2:
            dado_str = f"{byte_baixo:02X}"
            self.tela_barramento_endereco.setStyleSheet(self.barramento_inativo_style)
            self.tela_barramento_dados.setText(f"➡️ CPU envia o Byte baixo: 0x{dado_str}")
            self.tela_barramento_dados.setStyleSheet(self.barramento_ativo_style)
            self.memoria[self.demonstracao_endereco_calculado] = byte_baixo
            
            self.acesso_memoria("Escrita", f"{self.demonstracao_endereco_calculado:X}", dado_str, "(Byte Baixo)")
            
            self.demonstracao_passo_interno = 3
            return False
        if self.demonstracao_passo_interno == 3:
            self.demonstracao_label_ds.setStyleSheet(self.cor_borda_style)
            registrador_offset_label.setStyleSheet(self.cor_borda_style)
            self.tela_barramento_endereco.setText(f"Escrita (DST): Identificando DS e {registrador_offset_nome}+1 (p/ Byte Alto)")
            self.tela_barramento_endereco.setStyleSheet(self.barramento_ativo_style)
            self.tela_barramento_dados.setStyleSheet(self.barramento_inativo_style)
            self.demonstracao_passo_interno = 4
            return False
            
        elif self.demonstracao_passo_interno == 4:
            segmento = int(self.demonstracao_label_ds.text(), 16)
            offset = int(registrador_offset_label.text(), 16) + 1
            
            self.demonstracao_endereco_calculado = (segmento * 16) + offset
            calculo_str = f"Cálculo (DST): (DS * 16) + {registrador_offset_nome}+1\n(0x{segmento:X} * 16) + 0x{offset:X} = 0x{self.demonstracao_endereco_calculado:X}"
            
            self.tela_barramento_endereco.setText (f"➡️ {calculo_str}")
            self.tela_barramento_endereco.setStyleSheet(self.barramento_ativo_style)
            self.tela_barramento_dados.setStyleSheet(self.barramento_inativo_style)
            self.demonstracao_passo_interno = 5
            return False
        
        elif self.demonstracao_passo_interno == 5:
            dado_str = f"{byte_alto:02X}"
            self.tela_barramento_endereco.setStyleSheet(self.barramento_inativo_style)
            self.tela_barramento_dados.setText(f"➡️ CPU envia o Byte alto: 0x{dado_str}")
            self.tela_barramento_dados.setStyleSheet(self.barramento_ativo_style)
            self.memoria[self.demonstracao_endereco_calculado] = byte_alto
    
            self.acesso_memoria("Escrita", f"{self.demonstracao_endereco_calculado:X}", dado_str, "(Byte Alto)")

            self.demonstracao_passo_interno = 0
            return True
        return False
        
    def pegar_demonstracao_label(self, registrador_nome):
        registrador_nome = registrador_nome.upper().strip("[]") 
        if registrador_nome == "AX": return self.demonstracao_label_ax
        if registrador_nome == "BX": return self.demonstracao_label_bx
        if registrador_nome == "CX": return self.demonstracao_label_cx
        if registrador_nome == "DX": return self.demonstracao_label_dx
        if registrador_nome == "SI": return self.demonstracao_label_si
        if registrador_nome == "DI": return self.demonstracao_label_di
        if registrador_nome == "BP": return self.demonstracao_label_bp
        return QLabel("Erro")
        
    def resetar_demonstracao(self):
        widgets = [
            self.demonstracao_label_ax, self.demonstracao_label_bx, self.demonstracao_label_cx, self.demonstracao_label_dx,
            self.demonstracao_label_cs, self.demonstracao_label_ss, self.demonstracao_label_ds, self.demonstracao_label_es,
            self.demonstracao_label_ip, self.demonstracao_label_sp, self.demonstracao_label_bp, self.demonstracao_label_di,
            self.demonstracao_label_si, self.demonstracao_label_flag, self.memoria_edicao_ef, self.memoria_edicao_valor
        ]
        for widget in widgets:
            widget.setStyleSheet("")
            
        self.tela_barramento_endereco.setStyleSheet(self.barramento_inativo_style)
        self.tela_barramento_dados.setStyleSheet(self.barramento_inativo_style)
        
    def Registradores(self, funcao):
        self.instrução_atual = funcao
        self.label_resultado.setText(f"Executando: {funcao}")
        self.menu_stack.setCurrentIndex(6)
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Interface()
    ex.show()
    sys.exit(app.exec_())
