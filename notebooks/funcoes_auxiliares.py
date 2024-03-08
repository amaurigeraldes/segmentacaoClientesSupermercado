# ============================================================================================================ 
# CRIANDO UM GRÁFICO GENÉRICO PARA SER UTILIZADO SEMPRE QUE FOR NECESSÁRIO DETERMINAR A QUANTIDADE DE CLUSTERS 
# ============================================================================================================
# IDEALMENTE DEVERÁ SER SALVA NA PASTA Scripts do Ambiente Virtual criado para o Projeto
# ============================================================================================================

# Importando as bibliotecas
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from matplotlib.colors import ListedColormap

# Criando a Function graficos_elbow_silhouette
# Obs.1: A variável X deverá ser passada como parâmetro para definir as colunas do gráfico 
# Obs.2: O parãmetro random_state deverá ser informado se desejar que seja diferente de random_state = 42
# Obs.3: O parãmetro intervalo_k deverá ser informado se desejar que seja diferente de intervalo_k = (2, 11)
def graficos_elbow_silhouette(X, random_state = 42, intervalo_k = (2, 11)):

    # Criando uma figura com 2 sistemas de eixos sendo 1 linha e 2 colunas 
    # Obs.: usando tight_layout = True para os gráficos se ajustarem evitando a sobreposição
    fig, axs = plt.subplots(nrows = 1, ncols = 2, figsize = (16, 6), tight_layout = True)

    # Criando uma estrutura de dados, um dicionário vazio para o gráfico do cotovelo
    elbow = {}

    # Criando uma estrutura de dados, uma lista vazia para o gráfico da silhouette
    silhouette = []

    # Criando uma variável com um range de 2 a 10 (11 exclusive)
    # Obs.: fazendo um teste de 2 a 10 para definir qual é o melhor valor de k para criação dos clusters
    k_range = range(*intervalo_k) # fazendo um Unpacking Implícito (*), pois os valores estão dentro de uma Tupla

    # Percorrendo a variável x em k_range
    for i in k_range:
        # Aplicando o algoritmo e atribuindo à variável "kmeans"
        kmeans = KMeans(n_clusters = i, random_state = random_state, n_init = 10)
        # Fazendo o fit do Modelo
        kmeans.fit(X)
        # Passando para o gráfico elbow a chave "i" que indica o número de clusters e o kmeans.inertia_
        elbow[i] = kmeans.inertia_
        # Passando para o gráfico silhouette os rótulos(labels)
        labels = kmeans.labels_
        # Fazendo um append para o silhouette os parâmetros silhouette_score(X, labels)
        silhouette.append(silhouette_score(X, labels))

    # Plotando o gráfico de linhas do seaborn elbow(cotovelo)
    # Obs.1: passando no parâmetro x uma lista das chaves do dicionário
    # Obs.2: passando no parâmetro y uma lista dos valores do dicionário
    # Obs.3: passando no parâmetro ax a posição de índice 0 para o sistema de eixos
    sns.lineplot(x = list(elbow.keys()), y = list(elbow.values()), ax = axs[0])
    # Definindo o rótulo do Eixo X
    axs[0].set_xlabel("K")
    # Definindo o rótulo do Eixo Y
    axs[0].set_xlabel("Inertia")
    # Definindo o título para o gráfico
    axs[0].set_title("Elbow Method")

    # Plotando o gráfico de linhas do seaborn silhouette
    # Obs.1: passando no parâmetro x uma lista do k_range
    # Obs.2: passando no parâmetro y é o resultado da lista silhouette
    # Obs.3: passando no parâmetro ax a posição de índice 1 para o sistema de eixos
    sns.lineplot(x = list(k_range), y = silhouette, ax = axs[1])
    # Definindo o rótulo do Eixo X
    axs[1].set_xlabel("K")
    # Definindo o rótulo do Eixo Y
    axs[1].set_xlabel("Silhouette Score")
    # Definindo o título para o gráfico
    axs[1].set_title("Silhouette Method")

    # Exibindo o gráfico
    plt.show()
    



    
    
# Criando uma Figura Completa com projeção em 3 Dimensões
# Obs.: tornando a função mais genérica para poder ser utilizada em quaisquer outros Scripts


# Criando uma função para a visualização dos clusters
# Obs.: passando os parâmetros para a função
def visualizar_clusters(
    dataframe,
    colunas,
    quantidade_cores,
    centroids,
    mostrar_centroids = True, 
    mostrar_pontos = False,
    coluna_clusters = None
):
    
    # Criando a figura
    fig = plt.figure()
    # Criando um sistema de eixos e adicionando um subplot à figura
    # Obs.: passando o parâmentro 111, projection="3d" para gerar o gráfico 3D (ver documentação do matplotlib)
    ax = fig.add_subplot(111, projection = "3d")
    # Atribuindo à variável "cores" a quantidade de cores a serem utilizadas do color map da paleta de cores tab10 do matplotlib
    # Obs.: funciona para qualquer quantidade de cores que for passada como parâmetro da função
    cores = plt.cm.tab10.colors[:quantidade_cores]
    # Sobreescrevendo a variável cores passando a variável cores original para o ListedColormap(cores)
    cores = ListedColormap(cores)
    # Definindo a lista de colunas do DataFrame de acordo com os índices, colunas Age, Annual Income (k$) e Spending Score (1-100)
    x = dataframe[colunas[0]]
    y = dataframe[colunas[1]]
    z = dataframe[colunas[2]]
    
    # Mostrar os Centróides: usar parâmetro True
    ligar_centroids = mostrar_centroids
    # Mostrar os Pontos: usar parâmetro True
    ligar_pontos = mostrar_pontos
    
    # Percorrendo as variáveis "i" e "centroid" em enumerate(centroids)
    for i, centroid in enumerate(centroids):
        # Se for verdadeiro
        if ligar_centroids: 
            # Mostrando as coordenadas dos pontos x, y e z no gráfico de dispersão
            # Obs.: fazendo o Unpacking Implícito, passando o tamanho dos pontos no parâmetro s = 500 e alpha = 0.5
            ax.scatter(*centroid, s = 500, alpha = 0.5)
            # Mostrando nas coordenadas os números dos clusters
            # Obs.:passando os parâmetros tamanho da fonte e alinhamento horizontal/vertical
            ax.text(*centroid, f"{i}", fontsize = 20, horizontalalignment = "center", verticalalignment = "center")
        # Se for verdadeiro
        if ligar_pontos:
            # Mostrando todos os demais pontos e atribuindo à variável "s" (s de scatter)
            # Obs.1: definindo as cores no parâmetro c = coluna_clusters
            # Obs.2: ajustando o mapa de cores no parâmetro cmap = cores
            s = ax.scatter(x, y, z, c = coluna_clusters, cmap = cores)
            # Passando os parãmetros de legenda do gráfico de dispersão
            # Obs.: ajustando a posição da legenda, fazendo a ancoragem de legenda para não sobrepor o gráfico: bbox_to_anchor = (1.3, 1)
            ax.legend(*s.legend_elements(), bbox_to_anchor = (1.35, 1))
    
    # Definindo o Rótulo dos Eixos x, y e z de acordo com os índices, sendo Age, Annual Income (k$) e Spending Score (1-100) respectivamente
    ax.set_xlabel(colunas[0])
    ax.set_ylabel(colunas[1])
    ax.set_zlabel(colunas[2])
    # Definindo o Título 
    ax.set_title("Viewing the Clusters")
    # Exibindo o gráfico
    plt.show()