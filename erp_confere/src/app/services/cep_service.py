from models.cep_model import CepModel
import app_util.cep_request as viacep

def verify_cep(cep_from_client):

	num_cep = cep_from_client.replace('-', '')

	cep = CepModel.query_by_id(num_cep)

	if cep is None:
		return viacep.get_cep(num_cep)

	return cep