import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from matplotlib import rcParams

# Configuración de estilo
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("viridis")
rcParams['toolbar'] = 'None'  # Quita la barra de herramientas

class MapeoCompetencias:
    def __init__(self, archivo_excel):
        self.archivo = archivo_excel
        self.datos = None
        self.matriz = None
        self.asignaturas_info = None
        
    def cargar_datos(self, hoja):
        print(f"Cargando datos desde: {self.archivo}")
        
        self.datos = pd.read_excel(self.archivo, sheet_name=hoja, index_col=0)
        self.datos.index = self.datos.index.str.strip()
        self.datos.columns = self.datos.columns.str.strip()
        self.datos = self.datos.apply(pd.to_numeric, errors='coerce').fillna(0)
        self._ordenar_por_curso()
        return True
    
    def _ordenar_por_curso(self):
        columnas = self.datos.columns.tolist()
        
        def obtener_curso(nombre):
            partes = nombre.split('_')
            if len(partes) >= 1:
                try:
                    return int(partes[0].replace('º', '').replace('C', ''))
                except ValueError:
                    return 99
            return 99
        
        columnas_ordenadas = sorted(columnas, key=obtener_curso)
        self.matriz = self.datos[columnas_ordenadas]
        self.asignaturas_info = pd.DataFrame({'asignatura': columnas_ordenadas,
                                              'curso': [obtener_curso(c) for c in columnas_ordenadas]})
    
    def generar_heatmap(self, guardar, mostrar, separadoresCurso, leyenda, archivo_salida):
        n_asignaturas = len(self.matriz.columns)
        n_competencias = len(self.matriz.index)
        ancho = max(14, n_asignaturas * 0.6)
        alto = max(8, n_competencias * 0.4)
        fig, ax = plt.subplots(figsize=(ancho, alto))
        
        cmap = sns.color_palette([
            "#f7f7f7",  # Blanco (no trabaja)
            "#fee8c8",  # Amarillo claro (introducción)
            "#fdbb84",  # Naranja (desarrollo)
            "#e34a33",  # Rojo (dominio)
        ], as_cmap=True)
        
        sns.heatmap(
            self.matriz,
            annot=True,  # Mostrar valores
            fmt='.0f',   # Sin decimales
            cmap=cmap,linewidths=0.5,linecolor='white',
            cbar_kws={'label': 'Nivel de Trabajo','ticks': [0, 1, 2, 3],'shrink': 0.8},
            vmin=0,vmax=3,ax=ax
        )

        ax.set_xlabel('\nAsignaturas (ordenadas por curso)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Competencias Transversales\n', fontsize=12, fontweight='bold')
        plt.xticks(rotation=45, ha='right', fontsize=9)
        plt.yticks(rotation=0, fontsize=9)
        plt.title('Heatmap de competencias\n', fontsize=14, fontweight='bold', pad=20)
        plt.tight_layout()

        if separadoresCurso:
            cursos = self.asignaturas_info['curso'].values
            for i in range(1, len(cursos)):
                if cursos[i] != cursos[i-1]:
                    ax.axvline(x=i, color='black', linewidth=2, linestyle='--', alpha=0.7)
        
        if leyenda:
            leyenda_texto = ("Niveles: 0=No trabaja | 1=Introducción | 2=Desarrollo | 3=Dominio")
            fig.text(0.5, -0.02, leyenda_texto, ha='center', fontsize=10, 
                    style='italic', transform=fig.transFigure)
        
        if guardar:
            plt.savefig(archivo_salida, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
        
        if mostrar:
            plt.show()
        
        plt.close()

    def generar_estadisticas(self, guardar, mostrar, archivo_salida):
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Análisis de competencias\n', fontsize=16, fontweight='bold')
        
        # 1. Frecuencia por competencia
        freq = (self.matriz > 0).sum(axis=1).sort_values()
        colores = ['#e34a33' if v == 0 else '#2166ac' if v < 3 else '#1a9850' for v in freq]
        freq.plot(kind='barh', ax=axes[0,0], color=colores)
        axes[0,0].set(xlabel='Nº asignaturas', title='Frecuencia por Competencia\n(Rojo=Nunca | Azul=Poco | Verde=OK)')
        axes[0,0].axvline(x=3, color='orange', linestyle='--') # Minimo recomendado
        
        # 2. Carga por asignatura
        carga = self.matriz.sum(axis=0)
        carga.plot(kind='bar', ax=axes[0,1], color=plt.cm.RdYlGn(carga/carga.max()))
        axes[0,1].set(xlabel='Asignatura', ylabel='Suma niveles', title='Carga por Asignatura')
        axes[0,1].set_xticklabels(axes[0,1].get_xticklabels(), rotation=45, ha='right', fontsize=8)
        
        # 3. Distribución de niveles
        niveles = pd.Series(self.matriz.values.flatten()).value_counts().sort_index()
        colores3 = ['#f7f7f7', '#fee8c8', '#fdbb84', '#e34a33']
        niveles.plot(kind='bar', ax=axes[1,0], color=[colores3[int(i)] for i in niveles.index], edgecolor='black')
        axes[1,0].set(xlabel='Nivel', ylabel='Frecuencia', title='Distribución de Niveles')
        axes[1,0].set_xticklabels(['No trabaja', 'Introducción', 'Desarrollo', 'Dominio'], rotation=0)
        
        # 4. Evolución por curso
        evol = [{'Curso': f'{c}º', 'Total': self.matriz[self.asignaturas_info[self.asignaturas_info['curso']==c]['asignatura']].sum().sum()} 
                for c in sorted(self.asignaturas_info['curso'].unique())]
        df_evol = pd.DataFrame(evol)
        df_evol.plot(x='Curso', y='Total', kind='line', marker='o', ax=axes[1,1], 
                    linewidth=2, markersize=10, color='#2166ac', legend=False)
        axes[1,1].fill_between(range(len(df_evol)), df_evol['Total'], alpha=0.3, color='#2166ac')
        axes[1,1].set(ylabel='Suma total niveles', title='Intensidad por Curso')
        
        plt.tight_layout()
        
        if guardar:
            plt.savefig(archivo_salida, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
        
        if mostrar:
            plt.show()

        plt.close()

def main():
    # Verificar si existe el archivo de datos
    archivo_datos = "ejemplo.xlsx"
    
    if not Path(archivo_datos).exists():
        print("No se encontró excel.")
        return
    
    # Crear instancia y cargar datos
    mapeo = MapeoCompetencias(archivo_datos)
    
    if not mapeo.cargar_datos(hoja="CT_Asignaturas"):
        print("Error al cargar datos, comprueba el excel.") 
        return
    
    # 1. Heatmap de competencias
    mapeo.generar_heatmap(guardar=True, mostrar=False, separadoresCurso=True, leyenda=True, archivo_salida="heatmap_competencias.png")
    
    # 2. Análisis de competencias
    mapeo.generar_estadisticas(guardar=True, mostrar=False, archivo_salida="estadisticas_competencias.png")

if __name__ == "__main__":
    main()