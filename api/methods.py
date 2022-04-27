from base.models import User, Postoffice, Cartridge, Supply, Part, State, OPS, Supply_OPS, Part_OPS, State_OPS, Act, Group


def getinfo(data):
    params = dict()

    params.update({'count': 1})

    response = list()
    keys_response = ('version',)
    vals_response = ('0.1',)

    response.append(dict(zip(keys_response, vals_response)))

    return response, params



def getusers(data):
    params = dict()

    pars = dict()

    groups = data.get("groups_id", False)
    postoffices = data.get("postoffices_id", False)

    groups = [x for x in groups if isinstance(x, int)]

    if groups:
        pars.update({"group_id__in": groups})

    if postoffices:
        pars.update({"postoffice_id__in": postoffices})


    users = User.objects.filter(**pars)
    params.update({'count': users.count()})

    response = list()
    keys_response = ('id', 'username', 'role')

    all_rec = []
    for u in users:
        all_rec.append([u.id, u.username, u.role])

    for rec in all_rec:
        response.append(dict(zip(keys_response, rec)))

    return response, params



