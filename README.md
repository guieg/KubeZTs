# KubeZTs

Kubernetes Zero Trust Scanner (KubeZTs) é uma ferramenta desenvolvida para verificar a conformidade de clusters Kubernetes com os princípios do paradigma Zero Trust. A ferramenta realiza uma série de verificações de segurança automatizadas, assegurando que as configurações do cluster estejam corretas e em conformidade com as melhores práticas de segurança.

## Funcionalidades

- **Verificação de Habilitação de Auditoria**: Assegura que a auditoria esteja ativada e configurada corretamente.
- **Verificação do Uso de RBAC em vez de ABAC**: Garante que o RBAC esteja habilitado e o ABAC desativado.
- **Análise de Tráfego de Rede entre Pods**: Utiliza a extensão Ksniff para capturar e analisar pacotes transmitidos entre pods.
- **Detecção de Bind Desnecessário do Role ClusterAdmin**: Verifica se há contas de serviço ou usuários não autorizados com o role ClusterAdmin.
- **Verificação do Grupo system:masters**: Assegura que apenas o ClusterAdmin esteja incluído no grupo system:masters.
- **Verificação de Permissões Wildcard em Roles**: Identifica permissões wildcard em Roles e ClusterRoles não padrão.
- **Verificação de ResourceQuota em Todos os Namespaces**: Garante que todos os namespaces tenham um ResourceQuota configurado.
- **Verificação de LimitRange em Todos os Namespaces**: Assegura que todos os namespaces tenham um LimitRange especificado.
- **Verificação de Permissão de Listing Secrets**: Verifica se a permissão de listar segredos está restrita a usuários ou serviços autorizados.
## Requisitos

- Kubernetes cluster
- Acesso à API do Kubernetes
- Python 3.6+
- Kubectl instalado e configurado
- Extensão Ksniff para Kubectl

## Instalação

1. Clone o repositório:

```bash
git clone https://github.com/guieg/KubeZTs.git
cd KubeZTs
```

2. Instale as dependências:

```bash
pythom -m pip install -r requirements.txt
```

3. Configure a variável de ambiente KUBECONFIG para utilizar o kubeconfig desejado, você pode criar um arquivo .env:

```bash
# .env file
KUBECONFIG=".../path/to/kubeconfig
```

## Execução

```bash
python ./src/kubezts/main.py
```

# Contribuição

Contribuições são bem-vindas! Para contribuir com KubeZTs, siga os passos abaixo:

   1. Faça um fork do repositório.
   2. Crie uma branch para sua feature (git checkout -b feature/nova-feature).
   3. Commit suas mudanças (git commit -am 'Adiciona nova feature').
   4. Envie para o branch (git push origin feature/nova-feature).
   5. Abra um Pull Request.

# Licença


# Prova de conceito

Para que você possar testar a ferramenta, dentro da pasta poc há um Vagrantfile e um script ansible que criam um ambiente Kubernetes em máquinas virtuais, instalando através do kubeadm.

## Requisitos

1. Vagrant 2.3.6+
2. VirtualBox 7.0+
3. Ansible  2.16.6+



# Ambiente

Para iniciar esse ambiente siga os passos a seguir:

0. Entre no diretório da prova de conceito:

```bash
cd poc
```

1. Inicie as máquinas virtuais:

```bash
vagrant up
```

2. Execute o script ansible:

```bash
ansible-playbook -i inventory.yml setup_cluster.yml --ask-pass
```
> Utilize a senha "vagrant"

3. Agora é necessário obter o arquivo de configuração do cluster kubernetes, para isso execute os seguintes commandos:
```bash
vagrant ssh node1 # Acessa o nó 1 (master) via ssh
cp .kube/config /vagrant
exit
```
4. Agora o arquivo de configuração está na pasta poc e você pode utilizar ele setando a variável de ambiente:

```bash
export KUBECONFIG=.../path/to/KubeZTs/poc/config
```

5. Se o ambiente foi corretamente criado o comando seguinte deve dar a saída referente:

```bash
$ kubectl get nodes                                                                                                                 ✔  kubernetes-admin@kubernetes ⎈  06:10:09  
NAME    STATUS   ROLES           AGE    VERSION
node1   Ready    control-plane   5min   v1.30.1
node2   Ready    <none>          5min   v1.30.1
node3   Ready    <none>          5min   v1.30.1

```

## Remoção do ambiente

1. É possível desligar as máquinas virtuais com o comando:

```bash
vagrant halt
```

2. Caso deseje apagar as máquinas virtuais, utilize o comando:

```bash
vagrant destroy
```



