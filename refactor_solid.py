from abc import ABC, abstractmethod
from dataclasses import dataclass
import logging

# Setup logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

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
    oleh semua jenis processor pembayaran.
    
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
    oleh semua jenis layanan notifikasi.
    
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
    
    Kelas ini menangani logika spesifik untuk pembayaran kartu kredit.
    """
    
    def process(self, order: Order) -> bool:
        """Memproses pembayaran dengan kartu kredit.
        
        Args:
            order: Objek Order yang akan diproses
            
        Returns:
            True jika pembayaran kartu kredit berhasil
        """
        logging.info(f"Memproses pembayaran kartu kredit untuk {order.customer_name}")
        # Logika spesifik kartu kredit di sini
        return True


class EmailNotifier(INotificationService):
    """Implementasi layanan notifikasi melalui email.
    
    Kelas ini menangani pengiriman notifikasi melalui email.
    """
    
    def send(self, order: Order) -> None:
        """Mengirim notifikasi email konfirmasi.
        
        Args:
            order: Objek Order yang akan dikirim notifikasinya
        """
        logging.info(f"Mengirim email konfirmasi ke {order.customer_name}")
        # Logika pengiriman email di sini


class CheckoutService:
    """Service untuk mengkoordinasi proses checkout berdasarkan prinsip SRP.
    
    Kelas ini bertanggung jawab tunggal untuk mengkoordinasi proses checkout,
    termasuk pembayaran dan notifikasi.
    
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
    
    def run_checkout(self, order: Order) -> bool:
        """Menjalankan proses checkout lengkap.
        
        Metode ini mengkoordinasi proses pembayaran dan pengiriman notifikasi.
        
        Args:
            order: Objek Order yang akan diproses checkout
            
        Returns:
            True jika checkout berhasil, False jika gagal
        """
        logging.info(f"Memulai proses checkout untuk {order.customer_name}")
        
        # Proses pembayaran
        payment_success = self.payment_processor.process(order)
        
        if payment_success:
            order.status = "paid"
            self.notifier.send(order)
            logging.info(f"Checkout berhasil untuk {order.customer_name}")
            return True
        else:
            logging.warning(f"Checkout gagal untuk {order.customer_name}")
            return False


class QrisProcessor(IPaymentProcessor):
    """Implementasi processor pembayaran menggunakan QRIS.
    
    Kelas ini menangani logika spesifik untuk pembayaran QRIS.
    """
    
    def process(self, order: Order) -> bool:
        """Memproses pembayaran dengan QRIS.
        
        Args:
            order: Objek Order yang akan diproses
            
        Returns:
            True jika pembayaran QRIS berhasil
        """
        logging.info(f"Memproses pembayaran QRIS untuk {order.customer_name}")
        # Logika spesifik QRIS di sini
        return True