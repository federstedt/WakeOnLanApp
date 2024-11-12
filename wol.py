import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import socket


def create_payload(mac_addr: str):
    """
    Create Wake on Lan packet.
    """
    # clean up mac address from string to byte
    mac_clean = mac_addr.replace(":", "").replace("-", "")
    mac_bytes = bytes.fromhex(mac_clean)

    # create payload 0xFF = 255 x 6  FF:FF:FF:FF:FF:FF + mac-address x 16
    payload = b"\xff" * 6 + mac_bytes * 16
    return payload


def send_wol_l3(mac_addr: str, port: int = 9, target_ip: str = "<broadcast>"):
    """
    Send l3 wol packet using socket.

    args:
        mac_addr(str): Mac address in string format.
        port(int): udp port to send packet to, default is 9
        target_ip(str): Target ip subnet. default is broadcast of default interface.

    """
    payload = create_payload(mac_addr=mac_addr)

    # use socket to send packet
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        # Allow broadcast at socket layer
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        # send packet
        sock.sendto(payload, (target_ip, port))


class WakeOnLanApp:
    """
    The GUI App
    """

    def __init__(self, root):
        self.root = root
        self.root.title("WakeOnLan app")
        self.root.geometry("300x300")  # window size

        self.broadcast_entry_placeholder = "255.255.255.255"
        # theme
        style = ttk.Style()
        style.theme_use("default")

        # description label
        description_label = ttk.Label(root, text="Enter the MAC address below:")
        description_label.pack(pady=(10, 5))

        # entry
        self.mac_entry = ttk.Entry(root)
        self.mac_entry.insert(0, "mac-adress")  # Platshållartext
        self.mac_entry.config(foreground="grey")  # Grå text för platshållaren
        self.mac_entry.pack(pady=(0, 10))

        # Bind FocusIn och FocusOut-events
        self.mac_entry.bind("<FocusIn>", self.on_entry_click)
        self.mac_entry.bind("<FocusOut>", self.on_focus_out)

        # Broadcast ip optional text
        description_label_iptext = ttk.Label(root, text="Broadcast IP(Optional):")
        description_label_iptext.pack(pady=(10, 5))

        # entry for optional broadcast ip
        self.broadcast_entry = ttk.Entry(root)
        self.broadcast_entry.insert(0, self.broadcast_entry_placeholder)
        self.broadcast_entry.config(foreground="grey")
        self.broadcast_entry.pack(pady=(0, 10))

        # Binda FocusIn och FocusOut-events.
        self.broadcast_entry.bind("<FocusIn>", self.on_entry_click_bc)
        self.broadcast_entry.bind("<FocusOut>", self.on_focus_out_bc)

        # wake up button
        wake_button = ttk.Button(
            root, text="Wake up client", command=self.wake_up_client
        )
        wake_button.pack(pady=20)

    def wake_up_client(self):
        # check if main window still exists
        if self.root.winfo_exists():
            mac_address = self.mac_entry.get()
            broad_cast_ip = self.broadcast_entry.get()
            if mac_address and mac_address != "mac-adress":
                try:
                    if broad_cast_ip != self.broadcast_entry_placeholder:
                        # TODO: insert validator for ip-address format
                        send_wol_l3(mac_address, port=9, target_ip=broad_cast_ip)
                    else:
                        send_wol_l3(mac_address, port=9)
                    messagebox.showinfo(
                        "Wake On LAN", f"Sending WOL packet to: {mac_address}"
                    )
                except ValueError:
                    messagebox.showwarning("Input Error", "Invalid MAC address format")
            else:
                messagebox.showwarning(
                    "Input Error", "Please enter a valid MAC address."
                )

    # remove placeholder text when field is active
    def on_entry_click(self, event):
        if self.mac_entry.get() == "mac-adress":
            self.mac_entry.delete(0, "end")  # Rensa texten
            self.mac_entry.config(foreground="black")

    # add placeholder text if field is not active
    def on_focus_out(self, event):
        if self.mac_entry.get() == "":
            self.mac_entry.insert(0, "mac-adress")
            self.mac_entry.config(foreground="grey")

    # remove placeholder text when field is active
    def on_entry_click_bc(self, event):
        if self.broadcast_entry.get() == self.broadcast_entry_placeholder:
            self.broadcast_entry.delete(0, "end")  # Rensa texten
            self.broadcast_entry.config(foreground="black")

    # add placeholder text if field is not active
    def on_focus_out_bc(self, event):
        if self.broadcast_entry.get() == "":
            self.broadcast_entry.insert(0, self.broadcast_entry_placeholder)
            self.broadcast_entry.config(foreground="grey")


def main():
    root = tk.Tk()
    app = WakeOnLanApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
