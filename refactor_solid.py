from abc import ABC, abstractmethod
from dataclasses import dataclass
import logging

# Setup logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class Order:
    """Data class yang merepresentasikan pesanan pelanggan.
    
    Attributes:
        customer_name: Nama pelanggan yang melakukan pesanan
        total_price: Total harga dari pesanan
        status: Status pesanan, default adalah 'open'
    """
    customer_name: str
    total_price: float
    status: str = "open"


class IPaymentProcessor(ABC):
    """Interface untuk processor pembayaran berdasarkan prinsip DIP.
    
    Interface ini mendefinisikan kontrak yang harus diimplementasikan
    oleh semua jenis processor pembayaran berdasarkan prinsip Open-Closed.
    
    Methods:
        process: Memproses pembayaran untuk pesanan tertentu
    """
    
    @abstractmethod
    def process(self, order: Order) -> bool:
        """Memproses pembayaran untuk pesanan.
        
        Args:
            order: Objek Order yang akan diproses pembayarannya
            
        Returns:
            True jika pembayaran berhasil, False jika gagal
            
        Raises:
            Exception: Jika terjadi kesalahan dalam proses pembayaran
        """
        pass


class INotificationService(ABC):
    """Interface untuk layanan notifikasi berdasarkan prinsip DIP.
    
    Interface ini mendefinisikan kontrak yang harus diimplementasikan
    oleh semua jenis layanan notifikasi berdasarkan prinsip Open-Closed.
    
    Methods:
        send: Mengirim notifikasi kepada pelanggan
    """
    
    @abstractmethod
    def send(self, order: Order) -> None:
        """Mengirim notifikasi kepada pelanggan.
        
        Args:
            order: Objek Order yang menjadi konteks notifikasi
        """
        pass


class CreditCardProcessor(IPaymentProcessor):
    """Implementasi processor pembayaran menggunakan kartu kredit.
    
    Kelas ini menangani logika spesifik untuk pembayaran kartu kredit
    dan menunjukkan penerapan prinsip Single Responsibility.
    """
    
    def process(self, order: Order) -> bool:
        """Memproses pembayaran dengan kartu kredit.
        
        Args:
            order: Objek Order yang akan diproses
            
        Returns:
            True jika pembayaran kartu kredit berhasil
        """
        logger.info(f"Processing credit card payment for order: {order.customer_name}")
        try:
            # Simulasi logika pembayaran kartu kredit
            logger.debug(f"Amount to charge: ${order.total_price}")
            logger.info("Credit card payment processed successfully")
            return True
        except Exception as e:
            logger.error(f"Credit card payment failed: {str(e)}")
            return False


class EmailNotifier(INotificationService):
    """Implementasi layanan notifikasi melalui email.
    
    Kelas ini menangani pengiriman notifikasi melalui email
    dan menunjukkan penerapan prinsip Single Responsibility.
    """
    
    def send(self, order: Order) -> None:
        """Mengirim notifikasi email konfirmasi.
        
        Args:
            order: Objek Order yang akan dikirim notifikasinya
        """
        logger.info(f"Sending confirmation email to: {order.customer_name}")
        # Simulasi pengiriman email
        logger.debug(f"Email content: Order #{order.customer_name} confirmed")
        logger.info("Email notification sent successfully")


class CheckoutService:
    """Service untuk mengkoordinasi proses checkout berdasarkan prinsip SRP.
    
    Kelas ini bertanggung jawab tunggal untuk mengkoordinasi proses checkout,
    termasuk pembayaran dan notifikasi berdasarkan prinsip Dependency Injection.
    
    Attributes:
        payment_processor: Processor pembayaran yang diinject
        notifier: Layanan notifikasi yang diinject
    """
    
    def __init__(self, payment_processor: IPaymentProcessor, 
                 notifier: INotificationService):
        """Menginisialisasi CheckoutService dengan dependency injection.
        
        Args:
            payment_processor: Implementasi IPaymentProcessor untuk pembayaran
            notifier: Implementasi INotificationService untuk notifikasi
        """
        self.payment_processor = payment_processor
        self.notifier = notifier
        logger.debug(f"CheckoutService initialized with {type(payment_processor).__name__}")
    
    def run_checkout(self, order: Order) -> bool:
        """Menjalankan proses checkout lengkap.
        
        Metode ini mengkoordinasi proses pembayaran dan pengiriman notifikasi.
        
        Args:
            order: Objek Order yang akan diproses checkout
            
        Returns:
            True jika checkout berhasil, False jika gagal
        """
        logger.info(f"=== Starting checkout for customer: {order.customer_name} ===")
        logger.debug(f"Order details: Amount ${order.total_price}, Status: {order.status}")
        
        try:
            # Process payment
            logger.info("Processing payment...")
            payment_success = self.payment_processor.process(order)
            
            if payment_success:
                order.status = "paid"
                logger.info(f"Payment successful. Order status updated to: {order.status}")
                
                # Send notification
                logger.info("Sending notification...")
                self.notifier.send(order)
                
                logger.info(f"Checkout completed successfully for {order.customer_name}")
                return True
            else:
                logger.warning(f"Payment failed for customer: {order.customer_name}")
                return False
                
        except Exception as e:
            logger.error(f"Checkout process failed: {str(e)}")
            return False


class QrisProcessor(IPaymentProcessor):
    """Implementasi processor pembayaran menggunakan QRIS.
    
    Kelas ini menangani logika spesifik untuk pembayaran QRIS
    dan menunjukkan prinsip Open-Closed (OCP) dimana sistem dapat
    diperluas tanpa mengubah kode yang sudah ada.
    """
    
    def process(self, order: Order) -> bool:
        """Memproses pembayaran dengan QRIS.
        
        Args:
            order: Objek Order yang akan diproses
            
        Returns:
            True jika pembayaran QRIS berhasil
        """
        logger.info(f"Processing QRIS payment for order: {order.customer_name}")
        try:
            # Simulasi logika pembayaran QRIS
            logger.debug(f"Generating QR code for amount: ${order.total_price}")
            logger.info("QRIS payment processed successfully")
            return True
        except Exception as e:
            logger.error(f"QRIS payment failed: {str(e)}")
            return False


def main():
    """Fungsi utama untuk menjalankan demo sistem checkout.
    
    Fungsi ini menunjukkan penggunaan sistem dengan berbagai metode pembayaran
    dan mengilustrasikan penerapan prinsip SOLID dalam praktik.
    """
    
    logger.info("=== Starting Checkout System Demo ===")
    
    # Setup dependencies
    andi_order = Order("Andi", 500000)
    budi_order = Order("Budi", 100000)
    email_service = EmailNotifier()
    
    # Scenario 1: Credit Card Payment
    logger.info("\n--- Scenario 1: Credit Card Payment ---")
    cc_processor = CreditCardProcessor()
    checkout_cc = CheckoutService(
        payment_processor=cc_processor, 
        notifier=email_service
    )
    result1 = checkout_cc.run_checkout(andi_order)
    logger.info(f"Credit Card Checkout Result: {'SUCCESS' if result1 else 'FAILED'}")
    
    # Scenario 2: QRIS Payment (Demonstrasi OCP)
    logger.info("\n--- Scenario 2: QRIS Payment (OCP Demonstration) ---")
    qris_processor = QrisProcessor()
    checkout_qris = CheckoutService(
        payment_processor=qris_processor, 
        notifier=email_service
    )
    result2 = checkout_qris.run_checkout(budi_order)
    logger.info(f"QRIS Checkout Result: {'SUCCESS' if result2 else 'FAILED'}")
    
    logger.info("=== Checkout System Demo Completed ===")


if __name__ == "__main__":
    main()