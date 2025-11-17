#!/bin/bash
# Script para corregir imports y configuraciones

echo "🔧 Corrigiendo imports y configuraciones..."
echo ""

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 1. Corregir frontend/app.py
echo -e "${YELLOW}📝 Corrigiendo frontend/app.py...${NC}"
if [ -f "frontend/app.py" ]; then
    cp "frontend/app.py" "frontend/app.py.backup"
    sed -i 's/from services import data_base_mongo as db_mongo/import data_base_mongo as db_mongo/g' frontend/app.py
    echo -e "${GREEN}✅ frontend/app.py corregido${NC}"
else
    echo "⚠️  frontend/app.py no encontrado"
fi

# 2. Corregir services/service1/main.py
echo -e "${YELLOW}📝 Corrigiendo services/service1/main.py...${NC}"
if [ -f "services/service1/main.py" ]; then
    cp "services/service1/main.py" "services/service1/main.py.backup"
    sed -i 's/from services\.data_base_mongo import db/from data_base_mongo import db/g' services/service1/main.py
    sed -i 's/from services\.utils import serialize_mongo/from utils import serialize_mongo/g' services/service1/main.py
    echo -e "${GREEN}✅ services/service1/main.py corregido${NC}"
else
    echo "⚠️  services/service1/main.py no encontrado"
fi

# 3. Corregir my_agent/telegram_bot.py
echo -e "${YELLOW}📝 Corrigiendo my_agent/telegram_bot.py...${NC}"
if [ -f "my_agent/telegram_bot.py" ]; then
    cp "my_agent/telegram_bot.py" "my_agent/telegram_bot.py.backup"
    # Cambiar SERVICE2_URL hardcodeado por variable de entorno
    sed -i 's/SERVICE2_URL = "http:\/\/127\.0\.0\.1:8002"/SERVICE2_URL = os.getenv("SERVICE2_URL", "http:\/\/127.0.0.1:8003")/g' my_agent/telegram_bot.py
    echo -e "${GREEN}✅ my_agent/telegram_bot.py corregido${NC}"
else
    echo "⚠️  my_agent/telegram_bot.py no encontrado"
fi

# 4. Verificar que services/authentication/main.py no tenga imports problemáticos
echo -e "${YELLOW}📝 Verificando services/authentication/main.py...${NC}"
if [ -f "services/authentication/main.py" ]; then
    if grep -q "from services\." services/authentication/main.py; then
        cp "services/authentication/main.py" "services/authentication/main.py.backup"
        sed -i 's/from services\.data_base_mongo/from data_base_mongo/g' services/authentication/main.py
        sed -i 's/from services\.utils/from utils/g' services/authentication/main.py
        echo -e "${GREEN}✅ services/authentication/main.py corregido${NC}"
    else
        echo -e "${GREEN}✅ services/authentication/main.py OK${NC}"
    fi
fi

echo ""
echo -e "${GREEN}✅ Correcciones completadas!${NC}"
echo ""
echo "Archivos respaldados con extensión .backup"
echo ""
echo "📋 Resumen de cambios:"
echo "  1. frontend/app.py: import data_base_mongo as db_mongo"
echo "  2. service1/main.py: from data_base_mongo import db"
echo "  3. service1/main.py: from utils import serialize_mongo"
echo "  4. telegram_bot.py: SERVICE2_URL con variable de entorno"

