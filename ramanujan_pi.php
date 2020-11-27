<?php

$constantList = [
   // c1  	 	c2  	c3 	c4  c5      
    [1/8, 	 	20, 	3, 	-1, pow(4 * sqrt(2), 4)],
    [sqrt(3)/16, 	28, 	3, 	-1, pow(64 * sqrt(3), 2)],
    [1/72, 	 	260, 	23, 	-1, pow(12 * sqrt(2), 4)],
    [1/18/sqrt(11), 	280, 	19, 	 1, pow(12 * sqrt(11), 4)],
    [2/84/84, 		21460, 	1123, 	-1, pow(84 * sqrt(2), 4)],
    [1/2/sqrt(3), 	8, 	1, 	 1, pow(4 * sqrt(3), 4)],
    [2*sqrt(2)/9, 	10, 	1, 	 1, pow(12, 4)],
    [3*sqrt(3)/49, 	40, 	3, 	 1, pow(28, 4)],
    [sqrt(5)/288, 	644, 	41, 	-1, pow(1152*sqrt(5), 2)],
    [2*sqrt(2)/99/99, 	26390, 	1103, 	 1, pow(396, 4)],
];
define('TERMS', 20);

$target = 1 / pi();

foreach ($constantList as $list) {
    list($c1, $c2, $c3, $c4, $c5) = $list;
    $result = $c1;
    $sum = 0;

    for ($m = 0; $m < TERMS; $m++) {
        $sum += ($c2 * $m + $c3) * pow($c4, $m)
	        * factorial(4 * $m)
		/ pow($c5, $m) * pow(factorial($m), 4);
    }
    $result = $c1 * $sum;

    $diff = abs($target - $result);

    echo implode("\t", $list), "\t", $diff, PHP_EOL;
}

// factorial returns n!
function factorial($n) {
    if ($n == 1 || $n == 0) {
        return 1;
    }

    $result = 1;
    foreach(range(1, $n) as $n) {
        $result *= $n;
    }

    return $result;
}
