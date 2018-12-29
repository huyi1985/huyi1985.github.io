<?php
ini_set('memory_limit', '1024M');
$peers = isset($argv[1]) ? $argv[1] : 9;
$freq = array_pad([], $peers, 0);
// var_dump($freq);exit;

// The first three octets of the client IPv4 address are used as a hashing key. 
foreach (range(1, 255) as $i1) {
	foreach (range(1, 255) as $i2) {
		foreach (range(1, 255) as $i3) {
			$hash = hash_89_113_6271($i1, $i2, $i3);	
			// $hash = hash_2_3_5($i1, $i2, $i3);	
			// $hash = hash_7_11_13($i1, $i2, $i3);	
			// $hash = hash_djb("$i1.$i2.$i3");
			$index = $hash % $peers;
			$freq[$index] += 1;
		}
	}
}

var_dump(pow(255, 3), $freq, stddev($freq));

function hash_89_113_6271($i1, $i2, $i3) {
	$hash = 89;
	$hash = $hash * 113 + $i1 % 6271;
	$hash = $hash * 113 + $i2 % 6271;
	$hash = $hash * 113 + $i3 % 6271;

	return $hash;
}
	
function hash_2_3_5($i1, $i2, $i3) {
	$hash = 2;
	$hash = $hash * 3 + $i1 % 5;
	$hash = $hash * 3 + $i2 % 5;
	$hash = $hash * 3 + $i3 % 5;

	return $hash;
}
function hash_7_11_13($i1, $i2, $i3) {
	$hash = 7;
	$hash = $hash * 11 + $i1 % 13;
	$hash = $hash * 11 + $i2 % 13;
	$hash = $hash * 11 + $i3 % 13;

	return $hash;
}

function hash_djb($str) {
    for ($i = 0, $h = 5381, $len = strlen($str); $i < $len; $i++) {
        $h = (($h << 5) + $h + ord($str[$i])) & 0x7FFFFFFF;
    }
    return $h;
}

function stddev($a) {
	$n = count($a);
        $mean = array_sum($a) / $n;
        $carry = 0.0;
        foreach ($a as $val) {
            $d = ((double) $val) - $mean;
            $carry += $d * $d;
        };
        if ($sample) {
           --$n;
        }
        return sqrt($carry / $n);
}
