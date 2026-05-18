# ✂️ Sistema Barbearia

Sistema web completo para barbearias, construído com Django, HTML, CSS e JavaScript.  
Qualquer barbearia pode usar e personalizar através do painel administrativo.

---

## 🚀 Como rodar o projeto

### 1. Clone o repositório
```bash
git clone https://github.com/SEU_USUARIO/sistemabarbearia.git
cd sistemabarbearia
```

### 2. Crie e ative o ambiente virtual
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Rode as migrações
```bash
python manage.py migrate
```

### 5. Crie o superusuário (para acessar o painel admin)
```bash
python manage.py createsuperuser
```

### 6. Inicie o servidor
```bash
python manage.py runserver
```

Acesse em: **http://127.0.0.1:8000**  
Painel admin: **http://127.0.0.1:8000/admin**

---

## 🛠️ Tecnologias

- **Backend:** Python + Django
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **Ícones:** Bootstrap Icons
- **Fontes:** Google Fonts (Playfair Display + DM Sans)
- **Banco de dados:** SQLite (desenvolvimento)

---

## 📋 Funcionalidades

- ✅ Página Home com scroll suave (Hero, Serviços, Quem Somos, Equipe).
- ✅ Galeria de fotos dos cortes com lightbox.
- ✅ Filtro de galeria por barbeiro.
- ✅ Navbar responsiva com menu hamburguer.
- ✅ Links para Instagram e WhatsApp, add pelo admin.
- ✅ Painel administrativo quase completo (ainda comcluido dashboard)
- ✅ personalização do barbeiro ainda basica.


---

## ⚙️ Personalizações pelo Admin

Acesse `/admin` e configure:

| Seção | O que configurar |
|-------|-----------------|
| **Configuração da Barbearia** | Nome, slogan, foto hero, WhatsApp, Instagram |
| **Serviços** | Nome, descrição, preço, duração, ícone |
| **Barbeiros** | Nome, cargo, bio, foto, Instagram |
| **Fotos da Galeria** | Upload de fotos, vincular ao barbeiro, marcar destaque |

---


