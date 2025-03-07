import streamlit as st
import random
import urllib.parse

# Número de WhatsApp para enviar o pedido
WHATSAPP_NUMBER = "+5599991831701"

# Senha do dono do restaurante para visualizar os pedidos
ADMIN_PASSWORD = "1234"

# Inicializando session_state
if "carrinho" not in st.session_state:
    st.session_state["carrinho"] = []

if "pedidos" not in st.session_state:
    st.session_state["pedidos"] = []

# Dados do menu com URLs das imagens
MENU = {
    "Pizza Margherita": {"preco": 30.0, "imagem": "imagens/OIP__1_-removebg-preview.png"},
    "Hambúrguer Artesanal": {"preco": 25.0, "imagem": "imagens/11013540.png"},
    "Lasanha Bolonhesa": {"preco": 35.0, "imagem": "imagens/3c42feb1-9d73-4c03-bcdd-a496e59f4994-removebg-preview.png"},
    "Salada Caesar": {"preco": 20.0, "imagem": "imagens/chicken-caesar-salad.jpg"},
    "Sushi Combo": {"preco": 50.0, "imagem": "imagens/img_dueto-min.png"}
}

# Logo do restaurante
LOGO_URL = "imagens/logo.png"

def menu():
    """Tela do menu do restaurante."""
    st.image(LOGO_URL, width=100)
    st.title("Nosso Cardápio")
    search = st.text_input("Buscar no menu", "").lower()
    cols = st.columns(2)
    
    for index, (item, dados) in enumerate(MENU.items()):
        if search in item.lower():
            with cols[index % 2]:
                st.image(dados["imagem"], width=150)
                st.markdown(f"**{item}**")
                st.markdown(f"💲{dados['preco']:.2f}")
                quantidade = st.number_input(f"Quantidade de {item}", min_value=1, value=1, step=1, key=f"quantidade_{item}")
                if st.button(f"Adicionar {item}"):
                    for _ in range(quantidade):
                        st.session_state["carrinho"].append((item, dados['preco']))
                    st.success(f"{quantidade}x {item} adicionado(s) ao carrinho!")
    
    st.markdown("## Carrinho de Compras")
    if st.session_state["carrinho"]:
        total = 0
        itens = []
        for index, (item, preco) in enumerate(st.session_state["carrinho"]):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"- {item}: R$ {preco:.2f}")
            with col2:
                if st.button(f"❌", key=f"remover_{index}"):
                    st.session_state["carrinho"].pop(index)
                    st.rerun()
            itens.append(f"{item} (R$ {preco:.2f})")
            total += preco
        st.write(f"**Total: R$ {total:.2f}**")
        
        st.markdown("## Dados para Entrega")
        nome = st.text_input("Nome Completo")
        endereco = st.text_input("Endereço")
        telefone = st.text_input("Telefone")
        pagamento = st.selectbox("Forma de Pagamento", ["Pix", "Dinheiro", "Cartão de Crédito"])
        
        if st.button("Finalizar Pedido"):
            if nome and endereco and telefone:
                ticket_id = random.randint(1000, 9999)
                
                # Formatando a mensagem para WhatsApp
                itens_formatados = "\n".join([f"{item} (R$ {preco:.2f})" for item, preco in st.session_state["carrinho"]])
                total_formatado = f"R$ {total:.2f}"
                pedido_texto = f"""
Pedido {ticket_id}
Nome: {nome}
Endereço: {endereco}
Telefone: {telefone}
Itens:
{itens_formatados}
Total: {total_formatado}
Pagamento: {pagamento}
"""
                st.session_state["pedidos"].append(pedido_texto)
                
                # Codificando a mensagem para URL
                mensagem_whatsapp = urllib.parse.quote(pedido_texto)
                url_whatsapp = f"https://wa.me/{WHATSAPP_NUMBER}?text={mensagem_whatsapp}"
                st.markdown(f"[📲 Enviar Pedido pelo WhatsApp]({url_whatsapp})", unsafe_allow_html=True)
                st.success(f"Pedido realizado com sucesso! Ticket: {ticket_id}")
                st.session_state["carrinho"] = []
            else:
                st.error("Por favor, preencha todos os campos de entrega.")
    else:
        st.write("Carrinho vazio")

def main():
    st.set_page_config(page_title="Restaurante", layout="centered")
    
    menu_opcao = st.sidebar.radio("Navegação", ["Cardápio"])
    
    if menu_opcao == "Cardápio":
        menu()
    
    st.markdown("---")
    st.markdown("Desenvolvido por Nelson Alves")
    st.markdown("Siga-nos no Instagram: [@nelsonalvz_12](https://instagram.com/nelsonalvz_12)")

if __name__ == "__main__":
    main()
