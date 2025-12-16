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
        
        # Guardar información de cursos
        self.asignaturas_info = pd.DataFrame({
            'asignatura': columnas_ordenadas,
            'curso': [obtener_curso(c) for c in columnas_ordenadas]
        })
    
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
        
        # 1. Frecuencia de evaluación por competencia
        ax1 = axes[0, 0]
        frecuencia_competencias = (self.matriz > 0).sum(axis=1).sort_values()
        colores = ['#e34a33' if v == 0 else '#2166ac' if v < 3 else '#1a9850' 
                  for v in frecuencia_competencias.values]
        frecuencia_competencias.plot(kind='barh', ax=ax1, color=colores)
        ax1.set_xlabel('Número de asignaturas que la trabajan')
        ax1.set_title('Frecuencia de Trabajo por Competencia\n'
                     '(Rojo=Nunca | Azul=Poco | Verde=Adecuado)', fontsize=11)
        ax1.axvline(x=3, color='orange', linestyle='--', label='Mínimo recomendado')
        
        # 2. Carga por asignatura
        ax2 = axes[0, 1]
        carga_asignaturas = self.matriz.sum(axis=0)
        colores2 = plt.cm.RdYlGn([v/carga_asignaturas.max() for v in carga_asignaturas.values])
        carga_asignaturas.plot(kind='bar', ax=ax2, color=colores2)
        ax2.set_xlabel('Asignatura')
        ax2.set_ylabel('Suma de niveles de competencias')
        ax2.set_title('Carga de Competencias por Asignatura', fontsize=11)
        ax2.tick_params(axis='x', rotation=45)
        
        # 3. Distribución de niveles
        ax3 = axes[1, 0]
        niveles = self.matriz.values.flatten()
        niveles_conteo = pd.Series(niveles).value_counts().sort_index()
        colores3 = ['#f7f7f7', '#fee8c8', '#fdbb84', '#e34a33']
        bars = niveles_conteo.plot(kind='bar', ax=ax3, 
                                   color=[colores3[int(i)] for i in niveles_conteo.index],
                                   edgecolor='black')
        ax3.set_xlabel('Nivel')
        ax3.set_ylabel('Frecuencia')
        ax3.set_title('Distribución de Niveles de Trabajo', fontsize=11)
        ax3.set_xticklabels(['No trabaja', 'Introducción', 'Desarrollo', 'Dominio'], 
                           rotation=0)
        
        # 4. Evolución por curso
        ax4 = axes[1, 1]
        if self.asignaturas_info is not None:
            cursos_unicos = sorted(self.asignaturas_info['curso'].unique())
            evolucion = []
            for curso in cursos_unicos:
                asigs_curso = self.asignaturas_info[
                    self.asignaturas_info['curso'] == curso
                ]['asignatura'].tolist()
                if asigs_curso:
                    suma_curso = self.matriz[asigs_curso].sum().sum()
                    evolucion.append({'Curso': f'{curso}º', 'Total': suma_curso})
            
            df_evolucion = pd.DataFrame(evolucion)
            if not df_evolucion.empty:
                df_evolucion.plot(x='Curso', y='Total', kind='line', 
                                 marker='o', ax=ax4, linewidth=2, markersize=10,
                                 color='#2166ac', legend=False)
                ax4.fill_between(range(len(df_evolucion)), df_evolucion['Total'], 
                                alpha=0.3, color='#2166ac')
                ax4.set_ylabel('Suma total de niveles')
                ax4.set_title('Intensidad de Competencias por Curso', fontsize=11)
        
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