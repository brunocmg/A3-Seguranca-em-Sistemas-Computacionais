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
from PyQt5.QtCore import Qt

class Interface(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simulador de Instruções")
        self.setGeometry(400, 400, 800, 400)
        
        self.instrução_atual = None
        
        layout_inicial = QVBoxLayout(self)
        self.menu_stack = QStackedWidget()
        
        self.registrador_ax_input = QLineEdit()
        self.registrador_bx_input = QLineEdit()
        self.registrador_cx_input = QLineEdit()
        self.registrador_dx_input = QLineEdit()  
        
        self.registrador_cs_input = QLineEdit("4000")
        self.registrador_ss_input = QLineEdit("5000")
        self.registrador_ds_input = QLineEdit("6000")
        self.registrador_es_input = QLineEdit("7000")
        
        self.registrador_ip_input = QLineEdit()  
        self.registrador_sp_input = QLineEdit()  
        self.registrador_bp_input = QLineEdit()  
        self.registrador_di_input = QLineEdit()  
        self.registrador_si_input = QLineEdit()  

        self.registrador_flag_input = QLineEdit()  
        
        pagina_inicial = self.menu_principal()
        pagina_moves = self.menu_moves()
        pagina_arithmetic = self.menu_arithmetic()
        pagina_boolean = self.menu_boolean()
        pagina_compare = self.menu_compare()
        pagina_jxx = self.menu_jxx()
        pagina_registrador = self.menu_registradores()
        
        self.menu_stack.addWidget(pagina_inicial)
        self.menu_stack.addWidget(pagina_moves)
        self.menu_stack.addWidget(pagina_arithmetic)
        self.menu_stack.addWidget(pagina_boolean)
        self.menu_stack.addWidget(pagina_compare)
        self.menu_stack.addWidget(pagina_jxx)
        self.menu_stack.addWidget(pagina_registrador)
        
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
        btn_out.clicked.connect(lambda: self.execucao("Função OUT"))
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
        
        Box_Style = "QGroupBox { border: 1px solid black; border-radius: 5px;}"
        
        Box_Geral = QGroupBox("Registrador Geral")
        Box_Geral.setStyleSheet(Box_Style)
        Geral = QGridLayout()
        Geral.addWidget(QLabel("AX:"), 0, 0)
        Geral.addWidget(self.registrador_ax_input, 0, 1)
        Geral.addWidget(QLabel("BX:"), 1, 0)
        Geral.addWidget(self.registrador_bx_input, 1, 1)
        Geral.addWidget(QLabel("CX:"), 2, 0)
        Geral.addWidget(self.registrador_cx_input, 2, 1)
        Geral.addWidget(QLabel("DX:"), 3, 0)
        Geral.addWidget(self.registrador_dx_input, 3, 1)
        Box_Geral.setLayout(Geral)
        layout_2.addWidget(Box_Geral)
        
        Box_Segmentos = QGroupBox("Registrador de Segmentos")
        Box_Segmentos.setStyleSheet(Box_Style)
        Segmentos = QGridLayout()
        Segmentos.addWidget(QLabel("CS:"), 0, 0)  
        Segmentos.addWidget(self.registrador_cs_input, 0, 1)
        Segmentos.addWidget(QLabel("SS:"), 1, 0)    
        Segmentos.addWidget(self.registrador_ss_input, 1, 1)
        Segmentos.addWidget(QLabel("DS:"), 2, 0)
        Segmentos.addWidget(self.registrador_ds_input, 2, 1)
        Segmentos.addWidget(QLabel("ES:"), 3, 0)
        Segmentos.addWidget(self.registrador_es_input, 3, 1)
        Box_Segmentos.setLayout(Segmentos)
        layout_2.addWidget(Box_Segmentos)
        
        Box_Offsets = QGroupBox("Registrador de Offsets")
        Box_Offsets.setStyleSheet(Box_Style)
        Offsets = QGridLayout()
        Offsets.addWidget(QLabel("IP:"), 0, 0)
        Offsets.addWidget(self.registrador_ip_input, 0, 1)
        Offsets.addWidget(QLabel("SP:"), 1, 0)
        Offsets.addWidget(self.registrador_sp_input, 1, 1)
        Offsets.addWidget(QLabel("BP:"), 2, 0)
        Offsets.addWidget(self.registrador_bp_input, 2, 1)
        Offsets.addWidget(QLabel("DI:"), 3, 0)
        Offsets.addWidget(self.registrador_di_input, 3, 1)
        Offsets.addWidget(QLabel("SI:"), 4, 0)
        Offsets.addWidget(self.registrador_si_input, 4, 1)
        Box_Offsets.setLayout(Offsets)
        layout_2.addWidget(Box_Offsets)
        
        Box_Flag = QGroupBox("Registrador de Flags")
        Box_Flag.setStyleSheet(Box_Style)
        Flag = QGridLayout()
        Flag.addWidget(QLabel("FLAGS:"), 0, 0)
        Flag.addWidget(self.registrador_flag_input, 0, 1)
        Box_Flag.setLayout(Flag)
        layout_2.addWidget(Box_Flag)
        
        
        btn_voltar = QPushButton(" Voltar ao Menu Principal")
        btn_voltar.clicked.connect(lambda: self.menu_stack.setCurrentIndex(0))
        layout_2.addWidget(btn_voltar, alignment=Qt.AlignLeft)
        
        layout_2.addStretch(1)
        return pagina
    
    def Registradores(self, funcao):
        self.instrução_atual = funcao
        self.label_resultado.setText(f"Executando: {funcao}")
        self.menu_stack.setCurrentIndex(6)
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Interface()
    ex.show()
    sys.exit(app.exec_())
