import base64
import hmac
import hashlib
import json
import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)

class EsewaSandboxPayment:
    """
    eSewa Sandbox ePay v2 Gateway Integration for Nepal.
    Generates HMAC-SHA256 signature, validates success responses,
    and queries the eSewa status API.
    """
    SANDBOX_FORM_URL = getattr(settings, 'ESEWA_SANDBOX_URL', 'https://rc-epay.esewa.com.np/api/epay/main/v2/form')
    VERIFY_URL = getattr(settings, 'ESEWA_VERIFY_URL', 'https://rc.esewa.com.np/api/epay/transaction/status/')
    PRODUCT_CODE = getattr(settings, 'ESEWA_PRODUCT_CODE', 'EPAYTEST')
    SECRET_KEY = getattr(settings, 'ESEWA_SECRET_KEY', '8gBm/:&EnhH.1/q')

    @classmethod
    def generate_signature(cls, total_amount_str, transaction_uuid, product_code=None):
        """
        Creates HMAC-SHA256 signature for eSewa v2.
        Input string format: total_amount={amount},transaction_uuid={uuid},product_code={code}
        """
        code = product_code or cls.PRODUCT_CODE
        raw_message = f"total_amount={total_amount_str},transaction_uuid={transaction_uuid},product_code={code}"
        key = cls.SECRET_KEY.encode('utf-8')
        message = raw_message.encode('utf-8')
        signature_hash = hmac.new(key, message, hashlib.sha256).digest()
        return base64.b64encode(signature_hash).decode('utf-8')

    @classmethod
    def prepare_payment_form(cls, order, request):
        """
        Builds the parameters required to submit to the eSewa v2 form endpoint.
        """
        # Format total amount to 2 decimal places or integer if whole
        total_str = f"{order.total_amount:.2f}"
        transaction_uuid = f"{order.order_number}-{int(order.created_at.timestamp())}"
        
        # Build absolute URLs
        success_url = request.build_absolute_uri('/orders/esewa/success/')
        failure_url = request.build_absolute_uri('/orders/esewa/failure/')

        signature = cls.generate_signature(total_str, transaction_uuid, cls.PRODUCT_CODE)

        return {
            'action_url': cls.SANDBOX_FORM_URL,
            'amount': str(order.subtotal),
            'tax_amount': '0',
            'product_service_charge': '0',
            'product_delivery_charge': str(order.delivery_fee),
            'total_amount': total_str,
            'transaction_uuid': transaction_uuid,
            'product_code': cls.PRODUCT_CODE,
            'success_url': success_url,
            'failure_url': failure_url,
            'signed_field_names': 'total_amount,transaction_uuid,product_code',
            'signature': signature,
        }

    @classmethod
    def decode_and_verify_response(cls, encoded_data):
        """
        Decodes base64 response from eSewa and verifies the returned signature.
        """
        try:
            decoded_bytes = base64.b64decode(encoded_data)
            data = json.loads(decoded_bytes.decode('utf-8'))
            
            # eSewa response signed fields: e.g. transaction_code,status,total_amount,transaction_uuid,product_code,signed_field_names
            status = data.get('status')
            transaction_uuid = data.get('transaction_uuid')
            total_amount = data.get('total_amount')
            transaction_code = data.get('transaction_code', '')
            received_signature = data.get('signature', '')
            signed_field_names = data.get('signed_field_names', '')

            # Reconstruct message if signed_field_names provided
            if signed_field_names and received_signature:
                field_list = signed_field_names.split(',')
                parts = []
                for field in field_list:
                    val = data.get(field, '')
                    parts.append(f"{field}={val}")
                reconstructed_msg = ",".join(parts)
                key = cls.SECRET_KEY.encode('utf-8')
                expected_sig = base64.b64encode(hmac.new(key, reconstructed_msg.encode('utf-8'), hashlib.sha256).digest()).decode('utf-8')
                
                sig_valid = (expected_sig == received_signature)
            else:
                sig_valid = True

            return {
                'success': (status == 'COMPLETE' and sig_valid),
                'status': status,
                'transaction_uuid': transaction_uuid,
                'total_amount': total_amount,
                'transaction_code': transaction_code,
                'raw': data,
            }
        except Exception as e:
            logger.error(f"Error decoding eSewa response: {e}")
            return {'success': False, 'error': str(e)}

    @classmethod
    def verify_with_esewa_api(cls, product_code, total_amount, transaction_uuid):
        """
        Directly queries the eSewa Sandbox transaction status API endpoint.
        """
        params = {
            'product_code': product_code or cls.PRODUCT_CODE,
            'total_amount': str(total_amount),
            'transaction_uuid': transaction_uuid,
        }
        try:
            resp = requests.get(cls.VERIFY_URL, params=params, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                return data.get('status') == 'COMPLETE'
        except Exception as e:
            logger.warning(f"Could not reach external eSewa status API: {e}")
        return False
