# thread_monitor.py
"""
Utilitário para monitorar e listar threads ativas.
"""
import threading
from typing import List, Dict


class ThreadMonitor:
    """Utilitário para monitorar threads ativas."""

    @staticmethod
    def listar_threads_ativas() -> List[Dict[str, any]]:
        """
        Lista todas as threads ativas no programa.
        
        Returns:
            Lista de dicionários com informações sobre cada thread
        """
        threads_info = []
        
        for thread in threading.enumerate():
            info = {
                "nome": thread.name,
                "identificador": thread.ident,
                "viva": thread.is_alive(),
                "daemon": thread.daemon,
                "nativa": thread.native_id if hasattr(thread, 'native_id') else None
            }
            threads_info.append(info)
        
        return threads_info

    @staticmethod
    def imprimir_threads_ativas():
        """Imprime informações sobre todas as threads ativas."""
        threads = ThreadMonitor.listar_threads_ativas()
        
        if not threads:
            print("   ℹ Nenhuma thread encontrada.")
            return
        
        print(f"\n   📊 Threads ativas: {len(threads)}")
        print("   " + "=" * 70)
        
        for i, thread in enumerate(threads, 1):
            status = "✓ Viva" if thread["viva"] else "✗ Morta"
            daemon_status = "Daemon" if thread["daemon"] else "Normal"
            
            print(f"   [{i}] {thread['nome']}")
            print(f"       ID: {thread['identificador']}")
            print(f"       Status: {status} | Tipo: {daemon_status}")
            if thread["nativa"]:
                print(f"       Native ID: {thread['nativa']}")
            print()
        
        print("   " + "=" * 70)

    @staticmethod
    def contar_threads_ativas() -> int:
        """
        Retorna o número de threads ativas.
        
        Returns:
            Número de threads ativas
        """
        return threading.active_count()

    @staticmethod
    def obter_thread_por_nome(nome: str) -> threading.Thread:
        """
        Obtém uma thread pelo nome.
        
        Args:
            nome: Nome da thread a buscar
            
        Returns:
            Thread encontrada ou None
        """
        for thread in threading.enumerate():
            if thread.name == nome:
                return thread
        return None

