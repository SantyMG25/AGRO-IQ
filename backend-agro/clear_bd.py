import sqlite3


def reset_history():
    try:
        conn = sqlite3.connect("agro_iq.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print("🧹 Limpiando registros de AgroIQ...")
        for table in tables:
            table_name = table[0]
            cursor.execute(f"DELETE FROM {table_name};")
            cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{table_name}';")
            print(f"✔️ Tabla '{table_name}' vaciada con éxito.")
        conn.commit()
        print("✨ ¡Base de datos limpia y lista para nuevos escenarios!")
    except Exception as e:
        print(f"❌ Error al limpiar la base de datos: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    reset_history()
