#include
#include
#include

// Número máximo de candidatos
#define MAX 9

// Cada candidato tem um nome e uma contagem de votos
typedef struct
{
    string name;
    int votes;
} candidate;

candidate candidates[MAX];
int candidate_count;

// Protótipos das funções
bool vote(string name);
void print_winner(void);

int main(int argc, string argv[])
{
    // Verifica se foram passados candidatos
    if (argc < 2)
    {
        printf("Usage: plurality [candidate ...]\n");
        return 1;
    }

    // Preenche o array de candidatos
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i].name = argv[i + 1];
        candidates[i].votes = 0;
    }

    int voter_count = get_int("Number of voters: ");

    // Loop para ler os votos
    for (int i = 0; i < voter_count; i++)
    {
        string name = get_string("Vote: ");

        // Verifica se o voto é válido
        if (!vote(name))
        {
            printf("Invalid vote.\n");
        }
    }

    // Imprime o vencedor da eleição
    print_winner();
}

// Atualiza a contagem de votos se o candidato for encontrado
bool vote(string name)
{
    for (int i = 0; i < candidate_count; i++)
    {
        if (strcmp(candidates[i].name, name) == 0)
        {
            candidates[i].votes++;
            return true;
        }
    }
    return false;
}

// Imprime o vencedor (ou vencedores) da eleição
void print_winner(void)
{
    int max_votes = 0;

    // 1. Encontra o número máximo de votos entre todos os candidatos
    for (int i = 0; i < candidate_count; i++)
    {
        if (candidates[i].votes > max_votes)
        {
            max_votes = candidates[i].votes;
        }
    }

    // 2. Imprime todos os candidatos que têm o número máximo de votos
    for (int i = 0; i < candidate_count; i++)
    {
        if (candidates[i].votes == max_votes)
        {
            printf("%s\n", candidates[i].name);
        }
    }
}
