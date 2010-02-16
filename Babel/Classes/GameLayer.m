//
//  GameLayer.m
//  Genoma
//
//  Created by Giovanni Amati on 08/10/09.
//  Copyright 2009 __MyCompanyName__. All rights reserved.
//

#import "GameLayer.h"

@implementation GameLayer

-(id) init
{
	// always call "super" init
	// Apple recommends to re-assign "self" with the "super" return value
	if ((self = [super init]))
	{
		CCSprite *sprite = [CCSprite spriteWithFile:@"arena.png"];
		sprite.anchorPoint = CGPointZero;
		[self addChild:sprite z:0];
	}
	
	return self;
}

-(void) addMyCharacter:(NSArray *)attr position:(int)p
{
	NSString *fname = [[[NSString alloc] initWithFormat:@"%@", [attr objectAtIndex:1]] stringByAppendingString:@".png"];
	CCSprite *sprite = [CCSprite spriteWithFile:fname];
	sprite.scale = 0.4;
	sprite.anchorPoint = CGPointZero;
	sprite.position = ccp(125 - 25 * p, 150 - 35 * p);
	[self addChild:sprite z:p tag:10+p];
}

-(void) addEnemyCharacter:(NSArray *)attr position:(int)p
{
	NSString *fname = [[[NSString alloc] initWithFormat:@"%@", [attr objectAtIndex:1]] stringByAppendingString:@".png"];
	CCSprite *sprite = [CCSprite spriteWithFile:fname];
	sprite.scale = 0.4;
	sprite.scaleX = -0.4;
	sprite.anchorPoint = CGPointZero;
	sprite.position = ccp(350 + 25 * p, 150 - 35 * p);
	[self addChild:sprite z:p tag:20+p];
}

// on "dealloc" you need to release all your retained objects
-(void) dealloc
{	
	// in case you have something to dealloc, do it in this method
	// in this particular example nothing needs to be released.
	// cocos2d will automatically release all the children (Label)
	
	// don't forget to call "super dealloc"
	[super dealloc];
}

@end