<?php

interface Option {
	public function setServerOption(Server $server);
}

class TimeoutOption implements Option {
	private $timeout;
	public function __construct($timeout) {
		$this->timeout = $timeout;
	}
	public function setServerOption(Server $server) {
		$server->timeout = $this->timeout;
	}
	public function __invoke(Server $server) {
		$this->setServerOption($server);
        }
}

class MaxConnectionsOption implements Option {
	private $max;
	public function __construct($max) {
		$this->max = $max;
	}
	public function setServerOption(Server $server) {
		$server->maxConnections = $this->max;
	}
	public function __invoke(Server $server) {
		$this->setServerOption($server);
        }
}

class Server {
	private $address;
	/* !!PUBLIC!! */
	public $timeout;
	public $maxConnections;

	public function __construct($addr, Option ...$options) { 
		$this->address = $addr;
		foreach ($options as $option) {
			$option($this);
		}	
	}
}

$server = new Server("127.0.0.1:8001", new TimeoutOption(10), new MaxConnectionsOption(1000));
var_dump($server);


/*
object(Server)#1 (3) {
  ["address":"Server":private]=>
  string(14) "127.0.0.1:8001"
  ["timeout"]=>
  int(10)
  ["maxConnections"]=>
  int(1000)
}
*/
