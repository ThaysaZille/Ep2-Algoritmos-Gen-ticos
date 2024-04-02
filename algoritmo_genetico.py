import random
import copy

# Definindo os funcionários e suas habilidades
funcionarios = [
    {"nome": "João", "habilidades": ["Recepção", "Limpeza de Quartos"]},
    {"nome": "Maria", "habilidades": ["Cozinha", "Serviço de Quarto", "Bar"]},
    {"nome": "Ana", "habilidades": ["Recepção", "Lavanderia"]},
    {"nome": "Carlos", "habilidades": ["Limpeza de Quartos", "Manutenção"]},
    {"nome": "Bruno", "habilidades": ["Cozinha", "Serviço de Quarto"]},
    {"nome": "Paula", "habilidades": ["Recepção", "Limpeza de Quartos", "Bar"]},
    {"nome": "Pedro", "habilidades": ["Manutenção", "Limpeza de Quartos"]},
    {"nome": "Luiza", "habilidades": ["Lavanderia", "Limpeza de Quartos"]},
    {"nome": "Thiago", "habilidades": ["Cozinha", "Bar"]},
    {"nome": "Fernanda", "habilidades": ["Recepção", "Lavanderia", "Serviço de Quarto"]},
    {"nome": "Rafael", "habilidades": ["Cozinha", "Serviço de Quarto", "Bar"]},
    {"nome": "Juliana", "habilidades": ["Recepção", "Limpeza de Quartos"]},
    {"nome": "Caio", "habilidades": ["Manutenção", "Limpeza de Quartos"]},
    {"nome": "Beatriz", "habilidades": ["Recepção", "Limpeza de Quartos", "Serviço de Quarto"]},
    {"nome": "Lucas", "habilidades": ["Manutenção", "Limpeza de Quartos", "Bar"]},
    {"nome": "Bruna", "habilidades": ["Cozinha", "Serviço de Quarto"]},
    {"nome": "Marcelo", "habilidades": ["Recepção", "Limpeza de Quartos", "Lavanderia"]},
    {"nome": "Vanessa", "habilidades": ["Cozinha", "Bar"]},
    {"nome": "Danilo", "habilidades": ["Manutenção", "Limpeza de Quartos"]},
    {"nome": "Renata", "habilidades": ["Recepção", "Serviço de Quarto", "Bar"]}
]

# Definindo os turnos
turnos = ["Turno 1", "Turno 2", "Turno 3"]

# Função para inicializar a população
def inicializar_populacao(tamanho_populacao):
    populacao = []
    for _ in range(tamanho_populacao):
        individuo = []
        for turno in turnos:
            funcionarios_turno = random.sample(funcionarios, random.randint(1, len(funcionarios)))
            individuo.append(funcionarios_turno)
        populacao.append(individuo)
    return populacao

def calcular_aptidao(individuo):
    # Inicializar contadores
    total_funcionarios = 0
    habilidades_por_turno = {turno: [] for turno in turnos}
    sobreposicao_turnos = 0

    # Iterar sobre os turnos e funcionários alocados
    for turno, funcionarios_turno in enumerate(individuo):
        total_funcionarios += len(funcionarios_turno)

        # Verificar habilidades dos funcionários e contabilizar
        for funcionario in funcionarios_turno:
            habilidades_por_turno[turnos[turno]].extend(funcionario["habilidades"])

        # Verificar sobreposição de turnos
        if turno > 0:
            funcionarios_turno_anterior = tuple(funcionario["nome"] for funcionario in individuo[turno - 1])
            funcionarios_turno_atual = tuple(funcionario["nome"] for funcionario in funcionarios_turno)
            sobreposicao_turnos += len(set(funcionarios_turno_anterior) & set(funcionarios_turno_atual))

    # Calcular pontuação com base nos critérios
    pontuacao = 0
    # Critério 1: Minimizar o número total de funcionários
    pontuacao += total_funcionarios
    # Critério 2: Maximizar a distribuição adequada de habilidades
    for habilidades in habilidades_por_turno.values():
        pontuacao -= len(set(habilidades))  # Penalizar por habilidades duplicadas
    # Critério 3: Minimizar a sobreposição de turnos
    pontuacao += sobreposicao_turnos
    # Critério 4: Maximizar a cobertura de habilidades
    cobertura_habilidades = sum(len(set(habilidades)) for habilidades in habilidades_por_turno.values())
    pontuacao += cobertura_habilidades

    return pontuacao



# Função de seleção de pais por torneio
def selecao_por_torneio(populacao, k=3):
    torneio = random.sample(populacao, k)
    return max(torneio, key=calcular_aptidao)

# Função de seleção por tragédia
def selecao_por_tragedia(populacao, elite_percent=0.1):
    num_elite = int(len(populacao) * elite_percent)
    elite = sorted(populacao, key=calcular_aptidao)[:num_elite]
    fracasso = random.choice(populacao)
    return fracasso if random.random() < 0.5 else random.choice(elite)

# Função de mutação: Troca de funcionários entre dois turnos
def mutacao_troca_turno(individuo):
    mutante = copy.deepcopy(individuo)
    turno1, turno2 = random.sample(range(len(turnos)), 2)
    if mutante[turno1] and mutante[turno2]:  # Verifica se as listas de funcionários não estão vazias
        func1 = random.choice(mutante[turno1])
        func2 = random.choice(mutante[turno2])
        mutante[turno1].remove(func1)
        mutante[turno2].remove(func2)
        mutante[turno1].append(func2)
        mutante[turno2].append(func1)
    return mutante

# Função de mutação: Adicionar ou remover funcionário de um turno
def mutacao_adicionar_remover(individuo, taxa_adicionar=0.3, taxa_remover=0.3):
    mutante = copy.deepcopy(individuo)
    for i in range(len(turnos)):
        for func in funcionarios:
            if random.random() < taxa_adicionar and func not in mutante[i]:
                mutante[i].append(func)
            elif random.random() < taxa_remover and func in mutante[i]:
                mutante[i].remove(func)
    return mutante

# Função de crossover
def crossover(pai1, pai2):
    ponto_corte = random.randint(1, len(turnos) - 1)
    filho1 = pai1[:ponto_corte] + pai2[ponto_corte:]
    filho2 = pai2[:ponto_corte] + pai1[ponto_corte:]
    return filho1, filho2

# Parâmetros do algoritmo genético
tamanho_populacao = 65
taxa_mutacao = 0.1
taxa_crossover = 0.8
num_geracoes = 1000
geracoes_ate_tragedia = 1000

# Inicialização da população
populacao = inicializar_populacao(tamanho_populacao)

# Iteração do algoritmo genético
for geracao in range(num_geracoes):
    # Avaliação da aptidão de cada indivíduo
    aptidoes = [calcular_aptidao(individuo) for individuo in populacao]
    
    # Seleção dos pais
    if geracao < geracoes_ate_tragedia:
        selecionar_pais = selecao_por_torneio
    else:
        selecionar_pais = selecao_por_tragedia
    
    # Nova população
    nova_populacao = []
    
    # Crossover
    while len(nova_populacao) < tamanho_populacao:
        pai1 = selecionar_pais(populacao)
        pai2 = selecionar_pais(populacao)
        if random.random() < taxa_crossover:
            filho1, filho2 = crossover(pai1, pai2)
            nova_populacao.extend([filho1, filho2])
        else:
            nova_populacao.extend([pai1, pai2])
    
    # Mutação
    for i in range(len(nova_populacao)):
        if random.random() < taxa_mutacao:
            if random.random() < 0.5:
                nova_populacao[i] = mutacao_troca_turno(nova_populacao[i])
            else:
                nova_populacao[i] = mutacao_adicionar_remover(nova_populacao[i])
    
    # Atualização da população
    populacao = nova_populacao

# Exibindo o melhor indivíduo encontrado
melhor_individuo = max(populacao, key=calcular_aptidao)
print("Melhor indivíduo:")
for i, turno in enumerate(melhor_individuo):
    print(f"Turno {i+1}:")
    for funcionario in turno:
        print(f"  {funcionario['nome']}: {', '.join(funcionario['habilidades'])}")

print("Aptidão:", calcular_aptidao(melhor_individuo))
