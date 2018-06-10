def load_doc(path = 'petster-hamster.n3'):
    with open(path) as f:
        hamster_lines = f.readlines()
    return hamster_lines


def collect_data(hamster_lines):
    hamster_ids = [line.split(' ')[0].split(':')[1] for line in hamster_lines if 'foaf:Person' in line]
    hamster_friendship = [(line.split(' ')[0].split(':')[1], line.split(' ')[2].split(':')[1]) for line in hamster_lines if 'foaf:knows' in line]
    # [(i99,i98),(i1, i2)]
    # friendship_pair je tuple is hamster_friendship
    return hamster_ids, hamster_friendship


def create_friendship(hamster_ids, hamster_friendship):
    hamster_friendship_dict = dict()

    for hamster_id in hamster_ids:
        hamster_friendship_dict[hamster_id] = []
        # {i99:[i98, i1, i2, i10], i98:[i99], i999:[]}
        for friendship_pair in hamster_friendship:
            if friendship_pair[0] == hamster_id and friendship_pair[1] not in hamster_friendship_dict[hamster_id]:
                    hamster_friendship_dict[hamster_id].append(friendship_pair[1])
            elif friendship_pair[1] == hamster_id and friendship_pair[0] not in hamster_friendship_dict[hamster_id]:
                hamster_friendship_dict[hamster_id].append(friendship_pair[0])
    return hamster_friendship_dict
    # recnik za kljuceve ima id-jeve svih hrckova,
    #  a vrednosti su id-jevi svih onih koji su prijatelji.
    # npr 1:2,3,4,5 znaci da hrcak 1 ima za prijatelje hrcka 2, 3, 4 i 5
