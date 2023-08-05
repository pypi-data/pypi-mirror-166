#pragma once

#include "arch.h"
#include "net.h"

struct mip_driver {
  void (*init)(uint8_t *mac, void *data);           // Initialise driver
  size_t (*tx)(const void *, size_t, void *data);   // Transmit frame
  size_t (*rx)(void *buf, size_t len, void *data);  // Receive frame (polling)
  bool (*up)(void *data);                           // Up/down status
  // Set receive callback for interrupt-driven drivers
  void (*setrx)(void (*fn)(void *buf, size_t len, void *rxdata), void *rxdata);
};

struct mip_cfg {
  uint8_t mac[6];         // MAC address. Must not be 0
  uint32_t ip, mask, gw;  // IP, netmask, GW. If IP is 0, DHCP is used
};

void mip_init(struct mg_mgr *, struct mip_cfg *, struct mip_driver *, void *);

extern struct mip_driver mip_driver_stm32;
extern struct mip_driver mip_driver_enc28j60;

// Drivers that require SPI, can use this SPI abstraction
struct mip_spi {
  void *spi;                        // Opaque SPI bus descriptor
  uint8_t (*txn)(void *, uint8_t);  // SPI transaction: write 1 byte, read reply
  void (*begin)(void *);            // SPI begin: slave select low
  void (*end)(void *);              // SPI end: slave select high
};
