from paperswithcode import PapersWithCodeClient
from typing import Dict, Optional, Tuple
from secret import PWC_KEY
from paperswithcode.models.repository import Repositories
from paperswithcode.models.paper import Paper, Papers, Page


def get_repo_list(query: str = None) -> Optional[Repositories]:
    if query is not None:
        repository_list = client.repository_list(name=query)
        print(type(repository_list))
        return repository_list
    return None

def find_paper_from_selected_repo(selected_index: int, list: Repositories) -> Optional[Paper]:
    if list.results[selected_index].description != '':
        paper_query = list.results[selected_index].description 
        return client.paper_list(title=paper_query).results[0]
    
    return None

def print_list(list: Repositories) -> None:
    for idx, repo in enumerate(list.results):
        print(f"ID: [{idx}]\n{repo.name}\n{repo.owner}\n{repo.description}\n{repo.url}\n{'-' * 10}\n\n")


if __name__ == "__main__":
    '''This is strictly a test script'''
    client = PapersWithCodeClient(token=PWC_KEY)
    repos = client.repository_list()
    print(type(repos))
    # print(papers.next_page)
    exit()
    q = None
    while q != -1:
        q = input("Enter model name or -1 to exit: ")
        repo_list = get_repo_list(query=q)
        print_list(repo_list)
        # idx = input("Enter Selected Repo: ")
        # paper: Paper = find_paper_from_selected_repo(selected_index=int(idx), list=repo_list)
        # print(f"Paper Found:\nTitle: {paper.title}\nAuthors {paper.authors}\n{'-' * 10}\n\n")
        

