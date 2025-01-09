import PyPDF2
import pandas as pd
import re
from unidecode import unidecode

def extract_table_data(pdf_path):
    foro_dict = {
        'codigo': [],
        'descricao': []
    }
    
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        total_pages = len(reader.pages)
        print(f"Processando {total_pages} páginas...")
        
        for page_num in range(total_pages):
            print(f"Processando página {page_num + 1} de {total_pages}")
            text = reader.pages[page_num].extract_text()
            
            lines = text.split('\n')
            for line in lines:
                match = re.match(r'(\d+)\s+(.*)', line.strip())
                if match:
                    codigo = match.group(1)
                    descricao = match.group(2).strip()
                    
                    if len(codigo) >= 4 and any(palavra in descricao.lower() for palavra in ['foro', 'vara', 'tribunal', 'juizado', 'colegio', 'corregedoria', 'presidente', 'colégio recursal']):
                        foro_dict['codigo'].append(codigo)
                        foro_dict['descricao'].append(descricao)
    
    return pd.DataFrame(foro_dict)

def format_dataframe(df):
    df['descricao'] = df['descricao'].apply(lambda x: x.strip().title())
    df['codigo'] = df['codigo'].astype(str).str.zfill(4)
    
    df = df.sort_values('codigo')
    
    df = df.drop_duplicates()
    
    return df

def main():
    pdf_path = r'C:\Users\IsraelAntunes\Desktop\dic_foro_sp\UnidadesForunsSP.pdf'
    
    df = extract_table_data(pdf_path)
    
    df = format_dataframe(df)
    
    df.to_csv('foros_sp_codigos.csv', index=False, encoding='utf-8-sig')
    df.to_excel('foros_sp_codigos.xlsx', index=False)
    
    print("\nTabela de Códigos e Descrições dos Foros:")
    print("-" * 50)
    print(f"Total de unidades encontradas: {len(df)}")
    print("\nPrimeiras 5 entradas:")
    print(df.head())
    
    print("\nDistribuição por tipo:")
    tipos = df['descricao'].str.extract(r'(Foro|Vara|Tribunal|Juizado|Colégio|Corregedoria|Presidente|Colégio Recursal)', flags=re.IGNORECASE)[0]
    print(tipos.value_counts())

if __name__ == "__main__":
    main()
