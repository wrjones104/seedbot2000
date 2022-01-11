import json


def update_metrics(m):
    m_data = json.load(open('../db/metrics.json'))
    index = len(m_data) + 1
    m_data[index] = m
    with open('../db/metrics.json', 'w') as update_file:
        update_file.write(json.dumps(m_data))


def create_myseeds(x):
    with open('../db/myseeds.txt', 'w') as update_file:
        update_file.write(x)
    update_file.close()


def create_hardest(x):
    with open('../db/hardest.txt', 'w') as update_file:
        update_file.write(x)
    update_file.close()


def create_easiest(x):
    with open('../db/easiest.txt', 'w') as update_file:
        update_file.write(x)
    update_file.close()
